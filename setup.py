from setuptools import setup, find_packages

setup(
    name="Biomag TMS Experiment Dashboard",
    version="0.1.0",
    description="Interface gráfica em formato web para visualização e controle de eventos com o uso do InVesalius durante experimentos de TMS e EMG.",
    author="Carlo Rondinoni",
    author_email="crondi@alumni.usp.br",
    packages=find_packages(),
    install_requires=[
        "nicegui",
        "streamlit",
        "pandas",
        "numpy",
        "matplotlib",
        "Pillow",
        "altair",
        "python-socketio",
    ],
    python_requires='>=3.13.2',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
