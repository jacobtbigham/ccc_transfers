from pdfgrabber import PDFGrabber
from databasemaker import DatabaseMaker


def main():
    grabber = PDFGrabber(120, 'Software Engineering, B.S.', 'SWE', 0.2)
    grabber.get_pdfs()
    maker = DatabaseMaker('UCI', 'SWE')
    maker.add_classes()


if __name__ == '__main__':
    main()
