from tca_analysis.streamlit import StreamLitVisualisation


def main():
    file_path = '../data/tick_data'
    StreamLitVisualisation(file_path).perform_analysis()


if __name__ == "__main__":
    main()
    