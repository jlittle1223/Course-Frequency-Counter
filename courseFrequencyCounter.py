


url = "https://www.reg.uci.edu/perl/WebSoc"

outFileName = "courseOfferings.txt"


socEcolCourses = [
    "SocEcol  10",
    "SocEcol  13",
    "SocEcol  195",
    "SocEcol  195A",
    "SocEcol  195B",
    "SocEcol  111W",
    "SocEcol  183CW",
    "SocEcol  186CW",
    "SocEcol  H190W",
    "SocEcol  194W",
    "SocEcol  195CW",
    "SocEcol  195W"
    ]

crimCourses = []

for i in range(100, 192):
    crimCourses.append("Crm/Law  C" + str(i))


years = range(2013, 2019)

quarters = ["Fall Quarter",
            "Winter Quarter",
            "Spring Quarter", 
            "10-wk Summer",
            "Summer Session 1",
            "Summer Session 2"]

terms = []
for year in years:
    for quarter in quarters:
        terms.append("{} {}".format(year, quarter))

deptCourses = {"Crm/Law" : crimCourses, "SocEcol" : socEcolCourses}




def writeToFile(fileName:str, text:str):
    outFile = open(fileName, 'a')
    outFile.write(text)
    outFile.close()


def getDisplayTextResultsButton(driver):
    submitButtonsList = driver.find_elements_by_name("Submit")

    # WRONG
    # Need to find the submit button with the right name
    # Figure out how to find WebElement value
    return submitButtonsList[1]




def runWebCrawler():
    chromedriver = 'C:\\Users\\Jesse\\Documents\\Selenium\\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
        
    for department in deptCourses.keys():
        for year in years:
            for quarter in quarters:
                driver.get(url)
                    
                print("{} {} {}".format(year, quarter, department))

                departmentField = driver.find_element_by_name("Dept")
                departmentField.send_keys(department)

                departmentField = driver.find_element_by_name("YearTerm")
                departmentField.send_keys("{} {}".format(year, quarter))

                displayTextResultsButton = getDisplayTextResultsButton(driver)
                displayTextResultsButton.click()


                pageSource = driver.page_source
                for course in deptCourses[department]:
                    if course in pageSource:
                        print("Found {}".format(course))
                        offeringString = "{} $$$ {} $$$ {} $$$ {}\n".format(year, quarter, department, course)
                        writeToFile(outFileName, offeringString)

    driver.quit()


def runFrequencyAnalysis():

    inFile = open(outFileName, 'r')

    courseFrequency = {}
    for department in deptCourses.keys():
        for course in deptCourses[department]:
            for quarter in quarters:
                courseFrequency[(course, quarter)] = 0

    
    for department in deptCourses.keys():
        for course in deptCourses[department]:
            for quarter in quarters:
                inFile.seek(0)
                for line in inFile:
                    if course in line and quarter in line:
                        courseFrequency[(course, quarter)] += 1

    inFile.close()

    for department in deptCourses.keys():
        for course in deptCourses[department]:
            for quarter in quarters:
                courseCount = courseFrequency[(course, quarter)]
                courseFrequency[(course, quarter)] = float(courseCount) / float(len(years))
                print("Frequency of ({}) in quarter ({}) = {} ({} out of {})".format(course, quarter, courseFrequency[(course, quarter)], courseCount, len(years)))
                


if __name__ == "__main__":

    runWebCrawlerInput = input("Run Web Crawler? (Y/N): ").lower().strip()

    if runWebCrawlerInput == "y":
        import webbrowser
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        import re
        runWebCrawler()
        
    runFrequencyAnalysis()

        
    
                    
                
        

    


    
