soda:
	soda scan -d datawarehouse -c soda/configuration.yml soda/checks.yml

run:
	streamlit run dashboard.py