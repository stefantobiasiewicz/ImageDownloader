### Image Downloader:
Program downoads images form google graphic into output folder.

#### How to use:
Main parameters are placed in start of main function.
 - `keywords`: list of strings containig words to search in google search
 - `count`: number of images to download
 - `out`: path where images will be stored (if not exist will be created and if exist program clean directory before work)

#### Main program flow:
Script based on selenium e2e platform. 

 1. prepare output directory
 2. prepare searching url and web browser (firefox engine)
 3. browser go under prepared url and first page witch shows is google legal
    - script search and click skip button
 4. and before download image browser scroll down (and click load more button) to load images to fit count 
 5. start downloading.
 6. downloading proces consist of:
    - scrolling to specific image (for loading next images) 
    - downloading (two types): 
      - by url 
      - by base64
 
#### Details:

script find all html elements by css class, ex:
```
legal_button = driver.find_element(By.CSS_SELECTOR,
                                           '.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.Nc7WLe')
```

#### Developing:

Project to run needs all packages from `requirements.txt` file.

#### Author:
Stefan Tobiasiewicz 


