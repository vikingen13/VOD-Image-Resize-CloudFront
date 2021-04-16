
  const RESOLUTIONS = ['1080x1440','800x600','600x1080','720x480'];
  
  

function listImages(){

    const fetchPromise = fetch(location.href + "picList.json");
    fetchPromise.then(response => {
        console.log("1");
        return response.json();
    }).then(myJson => {
        console.log("2");
        console.log(myJson);

        myTable = document.getElementById('mainTable');
            //if no error, we list the images

            let myUrlParams = new URLSearchParams(window.location.search);
            let myImageList = []

            if( myUrlParams.has('img') ){
                //if param is present, we show only one image
                myImageList.push(myUrlParams.get('img'));
            }else{
                //we list all images
                for (const i in myJson['pics']) {
                    
                    myImageList.push(myJson['pics'][i]);
                      
                }  
            }


            for (const i in myImageList) {
                
                //In this case, we act
                mySmartRow = document.createElement('tr');
                myCenterRow = document.createElement('tr');

                for (const j in RESOLUTIONS) {
                    const element = RESOLUTIONS[j];
                    
                    myCell = document.createElement('td');
                    myImg = document.createElement('img');
                    myImg.setAttribute('src',element+'/'+myImageList[i]);
                    myImg.setAttribute('height','300px');
                    myImg.setAttribute("onclick", `copyToClipboard('${location.host}/${element}/${myImageList[i]}')`);

                    myCell.append(myImg);
                    mySmartRow.append(myCell);        

                    myCell = document.createElement('td');
                    myImg = document.createElement('img');
                    myImg.setAttribute('src',"center/"+element+'/'+myImageList[i]);
                    myImg.setAttribute('height','300px');
                    myImg.setAttribute("onclick", `copyToClipboard('${location.host}/center/${element}/${myImageList[i]}')`);

                    myCell.append(myImg);
                    myCenterRow.append(myCell);        

                    
                }

                myTable.append(mySmartRow);
                myTable.append(myCenterRow);
                

            }

    });



}

function copyToClipboard(aTextToCopy){
    let myTmpInput = document.createElement('input');

    document.getElementsByTagName('body')[0].append(myTmpInput);
    myTmpInput.value=aTextToCopy;
    myTmpInput.select();
    document.execCommand("copy");
    myTmpInput.remove();
    alert("URL copied to clipboard");
}

