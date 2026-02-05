import numpy as np


def apply_baseline(baseline_start_ms, baseline_end_ms, signal_start_ms, signal_end_ms, data, sampling_rate):
    """
    Aplica correção de baseline em um sinal.
    
    Args:
        baseline_start_ms: Início do intervalo de baseline em ms (ex: 5)
        baseline_end_ms: Fim do intervalo de baseline em ms (ex: 20)
        signal_start_ms: Início do sinal total em ms (ex: -10)
        signal_end_ms: Fim do sinal total em ms (ex: 40)
        data: Array com os dados do sinal
        sampling_rate: Taxa de amostragem em Hz
        
    Returns:
        Array com baseline corrigido
    """
    # Calcular número total de amostras
    total_samples = len(data)
    
    # Calcular índices do baseline
    # Converter tempo relativo ao início do sinal para índice do array
    baseline_start_idx = int((baseline_start_ms - signal_start_ms) * sampling_rate / 1000)
    baseline_end_idx = int((baseline_end_ms - signal_start_ms) * sampling_rate / 1000)
    
    # Garantir que os índices estão dentro dos limites
    baseline_start_idx = max(0, min(baseline_start_idx, total_samples - 1))
    baseline_end_idx = max(0, min(baseline_end_idx, total_samples))
    
    # Calcular baseline
    data_baseline = data[baseline_start_idx:baseline_end_idx]
    mean_baseline = np.mean(data_baseline)
    
    # Subtrair baseline de todo o sinal
    data_corrected = data - mean_baseline
    
    return data_corrected


def set_apply_baseline_all(baseline_start_ms, baseline_end_ms, signal_start_ms, signal_end_ms, data_windows, sampling_rate):
    """
    Aplica baseline em todas as janelas de dados.
    
    Args:
        baseline_start_ms: Início do intervalo de baseline em ms
        baseline_end_ms: Fim do intervalo de baseline em ms
        signal_start_ms: Início do sinal total em ms
        signal_end_ms: Fim do sinal total em ms
        data_windows: Lista de arrays com janelas de dados
        sampling_rate: Taxa de amostragem em Hz
        
    Returns:
        Lista de arrays com baseline corrigido
    """
    processed_data = []
    for window in data_windows:
        corrected = apply_baseline(
            baseline_start_ms, 
            baseline_end_ms, 
            signal_start_ms, 
            signal_end_ms, 
            window, 
            sampling_rate
        )
        processed_data.append(corrected)
    return processed_data

def new_indexes_fast_tol(A, B, decimals=5):
    """
    Retorna os índices de B cujas séries temporais
    não existem em A (com tolerância numérica).
    """
    A = np.asarray(A)
    B = np.asarray(B)

    # quantização (estável e rápida)
    Aq = np.round(A, decimals=decimals)
    Bq = np.round(B, decimals=decimals)

    # hash por linha
    set_A = {tuple(row) for row in Aq}

    # índices novos
    return [i for i, row in enumerate(Bq) if tuple(row) not in set_A]

def p2p_from_time(signal, fs, tmin_ms, start_ms=10):
    signal = np.asarray(signal)
    start_idx = int(round((start_ms - tmin_ms) * fs / 1000))
    cropped = signal[start_idx:]
    return round(np.ptp(cropped),2)