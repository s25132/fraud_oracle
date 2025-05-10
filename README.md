# fraud_oracle

### Założenia:
Instalacja bibliotek z requirements.txt
Na koncie usług google jest katalog raw_data z plikiem z danymi fraud_oracle

### Konfiguracja
Stworzyć plik .env i go wypełnić na podstawie .env_example.
Przeniesienie pliku autentykacji do service_account do katalogu conf/local/.

### Odpalenie patoku data_processing 
kedro run --pipeline data_processing

### Odpalenie patoku creating_model (bez parametru file_id potok pobierze najnowsze dane treningowe i testowe)
kedro run --pipeline creating_model

### Odpalenie patoku creating_model (z parametrem file_id potok pobierze dane treningowe i testowe z id fdcbd636)
kedro run --pipeline creating_model --params file_id=fdcbd636

### Budowa obrazu:
kedro docker build
 
### Odpalenie patoku data_processing z docker
kedro docker run --pipeline data_processing

### Odpalenie patoku creating_model (bez parametru file_id potok pobierze najnowsze dane treningowe i testowe) z docker
kedro docker run --pipeline creating_model

### Odpalenie patoku creating_model (z parametrem file_id potok pobierze dane treningowe i testowe z id fdcbd636) z docker
kedro docker run --pipeline creating_model --params file_id=fdcbd636
