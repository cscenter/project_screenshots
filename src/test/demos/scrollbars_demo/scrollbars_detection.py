from utils.screenshot import Screenshot
from utils.analyser_results import AnalyserResults
from screenshot_filters.scrollbars_detector import ScrollBarAnalyser
import cv2

if __name__ == '__main__':
    img1 = cv2.imread('1.png')
    img2 = cv2.imread('2.png')
    img3 = cv2.imread('3.png')
    img4 = cv2.imread('4.png')

    res1 = AnalyserResults()
    scr1 = Screenshot(img1, "", "", res1)
    analyser = ScrollBarAnalyser()
    analyser.execute(scr1)
    print("Results for 1.png:")
    scr1.result.print_results()

    res2 = AnalyserResults()
    scr2 = Screenshot(img2, "", "", res2)
    analyser.execute(scr2)
    print("Results for 2.png:")
    scr2.result.print_results()

    res3 = AnalyserResults()
    scr3 = Screenshot(img3, "", "", res3)
    analyser.execute(scr3)
    print("Results for 3.png:")
    scr3.result.print_results()

    res4 = AnalyserResults()
    scr4 = Screenshot(img4, "", "", res4)
    analyser.execute(scr4)
    print("Results for 4.png:")
    scr4.result.print_results()