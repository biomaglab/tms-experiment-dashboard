import socket
import struct
import time
import threading
from collections import deque

from tms_dashboard.constants import TriggerType

NEURONE_IP = '192.168.200.220'
DATA_PORT = 50000
JOIN_PORT = 5050
BUFFER_SIZE = 65535

class FrameType:
    MEASUREMENT_START = 1
    SAMPLES = 2
    TRIGGER = 3
    MEASUREMENT_END = 4
    JOIN = 128

class neuroOne:
    def __init__(self, num_trial: int, t_min, t_max, ch: int, trigger_type_interest: TriggerType):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.settimeout(0.1)  # Reduzido de 1.0s para melhor responsividade

        self.__connected = False
        self.__status_meansurament = False
        self.__buffer = deque(maxlen=100000)
        self.__lock = threading.Lock()
        self.__running = False
        self.__thread = None
        self.__first_sample_idx = None

        self.__num_channels = 0
        self.__sampling_rate = 0
        self.__pending_triggers = deque(maxlen=num_trial)
        self.__triggered_windows_data = deque(maxlen=num_trial)
        self.__ch_index_in_bundle = 0
        self.__scale_factor = 0.1
        
        # Detecção de perda de pacotes UDP
        self.__last_seq_no = None
        self.__packets_lost = 0

        self.t_min = t_min
        self.t_max = t_max
        self.ch = ch
        self.trigger_type_interest = trigger_type_interest

        try:
            self.__sock.bind(('', DATA_PORT))
        except Exception as e:
            print(f"Erro no Bind: {e}")
    
    def start(self):
        if not self.__running:
            self.__running = True
            self.__thread = threading.Thread(target=self.__listen_loop, daemon=True)
            self.__thread.start()

    def stop(self):
        self.__running = False
        self.__close_connection()
        if self.__thread:
            self.__thread.join()

    def __listen_loop(self):
        while self.__running:
            if not self.__connected:
                self.__try_connect()
                time.sleep(0.5)
                continue
            else:
                try:
                    data, addr = self.__sock.recvfrom(BUFFER_SIZE)
                    if data:
                        frame_type = data[0]
                        self.__process_pack(frame_type, data)
                        self.__update_triggered_window()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Erro na recepção: {e}")
            
    def get_connection(self):
        return self.__connected

    def get_status(self):
        return self.__status_meansurament
    
    def __try_connect(self):
        while not self.__connected:
            self.__send_join_packet()
            try:
                data, addr = self.__sock.recvfrom(BUFFER_SIZE)
                if not len(data) > 0:
                    self.__connected = True
                    print("Connected with NeuroOne")
            except:
                self.__connected = False

    def __send_join_packet(self):
        """ Envia o pacote JOIN para destravar o streaming do hardware """
        join_packet = struct.pack('>B3x', FrameType.JOIN) # Tipo 128 + 3 bytes padding
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(join_packet, (NEURONE_IP, JOIN_PORT))
        except Exception as e:
            print(f"Erro ao enviar JOIN: {e}")
        
    def __process_pack(self, frame_type, data):
        if frame_type == FrameType.MEASUREMENT_START:
            # Parse conforme StartPacketFieldIndex do C++
            self.__sampling_rate = struct.unpack('>I', data[4:8])[0]
            self.__num_channels = struct.unpack('>H', data[16:18])[0]
            self.__status_meansurament = True

            offset = 18
            found_idx = None
            for i in range(self.__num_channels):
                phys_id = struct.unpack('>H', data[offset:offset+2])[0]
                if phys_id == self.ch:
                    found_idx = i
                offset += 2

            if found_idx is not None:
                type_byte = data[offset + found_idx]
                is_dc = (type_byte & 0x07) == 1
                is_tesla = ((type_byte >> 3) & 0x03) == 1
                
                divider = 1.0
                if is_dc: divider = 100.0
                elif is_tesla: divider = 20.0 # Tesla AC divisor

                with self.__lock:
                    self.__scale_factor = 0.1 / divider
                    self.__ch_index_in_bundle = found_idx
                    self.__buffer = deque(maxlen=self.__sampling_rate * 3000)

        elif frame_type == FrameType.SAMPLES:
            if self.__num_channels == 0: return
            # Parse conforme SamplesPacketFieldIndex do C++
            seq_no = struct.unpack('>I', data[4:8])[0]
            sample_idx = struct.unpack('>Q', data[12:20])[0]
            num_bundles = struct.unpack('>H', data[10:12])[0]
            
            # Detectar perda de pacotes UDP
            with self.__lock:
                if self.__last_seq_no is not None:
                    expected = (self.__last_seq_no + 1) % (2**32)
                    if seq_no != expected:
                        lost = (seq_no - expected) % (2**32)
                        self.__packets_lost += lost
                        print(f"{lost} pacote(s) UDP perdido(s)! Total acumulado: {self.__packets_lost}")
                
                self.__last_seq_no = seq_no
            
            # As amostras começam no byte 28. Cada amostra tem 3 bytes (int24)
            offset = 28
            bytes_per_bundle = self.__num_channels * 3
            target_offset_in_bundle = self.__ch_index_in_bundle * 3

            with self.__lock:
                if self.__first_sample_idx is None:
                    self.__first_sample_idx = sample_idx
                
                for b in range(num_bundles):
                    # Pula direto para o byte do canal de interesse dentro do bundle
                    pos = offset + (b * bytes_per_bundle) + target_offset_in_bundle
                    sample_raw = data[pos : pos + 3]
                    val_uV = int24_to_int32(sample_raw) * self.__scale_factor
                    self.__buffer.append(val_uV)
                    
                    if len(self.__buffer) == self.__buffer.maxlen:
                        self.__first_sample_idx += 1

            
        elif frame_type == FrameType.MEASUREMENT_END:
            self.__status_meansurament = False
            self.__num_channels = 0
            self.__sampling_rate = 0
        
        elif frame_type == FrameType.TRIGGER:
            num_triggers = struct.unpack('>H', data[2:4])[0]
            offset = 8
            for _ in range(num_triggers):
                # Parse dos 20 bytes da estrutura Trigger
                sample_idx = struct.unpack('>Q', data[offset+8:offset+16])[0]
                type_byte  = data[offset+16]
                trigger_code = data[offset+17] # Código de 8 bits (0-255)

                # Extração dos tipos
                source_id = (type_byte >> 4) & 0x0F
                mode      = type_byte & 0x0F
                if mode == self.trigger_type_interest.value:
                    with self.__lock:
                        self.__pending_triggers.append({
                            'idx': sample_idx,
                            'code': trigger_code,
                        })
                        print(f"Trigger detectado: {TriggerType(mode).name} (Código: {trigger_code}) na amostra {sample_idx}")

                offset += 20
    
    def __update_triggered_window(self):
        with self.__lock:
            if self.__first_sample_idx is None: return
            
            n_pre = int(abs(self.t_min) * self.__sampling_rate)
            n_post = int(self.t_max * self.__sampling_rate)
            last_idx = self.__first_sample_idx + len(self.__buffer) - 1

            # Process triggers and mark which ones to remove
            triggers_to_remove = []
            
            for trig in self.__pending_triggers:
                end_sample = trig['idx'] + n_post
                if last_idx >= end_sample:
                    start_pos = (trig['idx'] - n_pre) - self.__first_sample_idx
                    end_pos = (trig['idx'] + n_post) - self.__first_sample_idx
                    
                    if start_pos >= 0:
                        window = list(self.__buffer)[start_pos:end_pos]
                        self.__triggered_windows_data.append(window)
                        triggers_to_remove.append(trig)
            
            # Remove processed triggers
            for trig in triggers_to_remove:
                self.__pending_triggers.remove(trig)
    
    def get_triggered_window(self):
        """Retorna cópia thread-safe das janelas capturadas."""
        if self.__connected and self.__status_meansurament and self.__running:
            with self.__lock:
                return list(self.__triggered_windows_data)
        return []
    
    def get_sampling_rate(self):
        return self.__sampling_rate
    
    def get_statistics(self):
        """Retorna estatísticas de conexão para debugging."""
        with self.__lock:
            return {
                'packets_lost': self.__packets_lost,
                'pending_triggers': len(self.__pending_triggers),
                'captured_windows': len(self.__triggered_windows_data),
                'buffer_size': len(self.__buffer),
                'sampling_rate': self.__sampling_rate
            }
        
    def get_pick2pick(self):
        if self.__connected and self.__status_meansurament and self.__running:
            with self.__lock:
                list(self.__triggered_windows_data)
                return list(self.__triggered_windows_data)
        return []
    
    def __close_connection(self):
        self.__sock.close()
        if self.__connected:
            self.__connected = False
            print("Disconnected from NeuroOne")

def int24_to_int32(data_bytes):
    """ 
    Converte 3 bytes (int24 big-endian) para int32 com sinal.
    Replica a lógica C++: (val[0]<<24 | val[1]<<16 | val[2]<<8) >> 8
    """
    # Monta o valor deslocado para a esquerda para preservar o sinal no bit 31
    combined = (data_bytes[0] << 24) | (data_bytes[1] << 16) | (data_bytes[2] << 8)
    
    # Em Python, precisamos simular o comportamento do shift aritmético de 32 bits
    if combined & 0x80000000: # Se o bit de sinal (MSB) estiver ativo
        return (combined >> 8) - (1 << 24)
    else:
        return combined >> 8


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    device = neuroOne(10, -0.01, 0.04, 33, TriggerType.STIMULUS)
    device.start()

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))

    try:
        while True:
            # Simulando o processamento dos dados coletados a cada 100ms
            windows = device.get_triggered_window()
            if windows is not None and len(windows)>0:
                ax.clear()
                # Cria o eixo do tempo baseado na janela definida
                # O ponto 0 será exatamente o trigger
                time_axis = np.linspace(device.t_min, device.t_max, len(windows[0]))
                
                for i, win in enumerate(windows):
                    alpha = 0.3 if i < len(windows)-1 else 1.0 # Destaque para a última
                    ax.plot(time_axis, win, alpha=alpha, label=f"Trial {i+1}" if i == len(windows)-1 else "")
                
                ax.axvline(0, color='red', linestyle='--', label='Trigger')
                ax.set_title(f"Janelas Capturadas (Total: {len(windows)}) - Canal {device.ch}")
                ax.set_xlabel("Tempo (s)")
                ax.set_ylabel("Amplitude (uV)")
                ax.grid(True)
                plt.draw()
                plt.pause(0.01)
            
            time.sleep(3)
    except KeyboardInterrupt:
        device.stop()
        print("Aplicação encerrada.")