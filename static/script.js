const form = document.querySelector("form"),
fileInput = document.querySelector(".file-input"),
progressArea = document.querySelector(".progress-area"),
uploadedArea = document.querySelector(".uploaded-area");
const process=document.querySelector("#process-reset");
var myFormName=document.getElementById("myForm");
var myfontformName=document.getElementById("myfontForm");
const fileInput2 = document.querySelector(".file-input-2");
const process_font=document.querySelector("#process-reset-font"),
progressAreaFont = document.querySelector(".progress-area-font"),
uploadedAreaFont = document.querySelector(".uploaded-area-font");
const process_font_submit=document.querySelector("#process-font");
process_font_submit.disabled=true;
const font_txt=document.querySelector("#font-txt");
font_txt.style.visibility="hidden";

myFormName.addEventListener("click", () =>{
  fileInput.click();
});
 var filePath,myFileName;
fileInput.onchange = ({target})=>{
  let file = target.files[0];
  if(file){
    let fileName = file.name;
    console.log(fileName)

    if(fileName.length >= 12){
      let splitName = fileName.split('.');
      fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
    }
    //  let fileLoaded = Math.floor((loaded / total) * 100);
    //let fileTotal = Math.floor(total / 1000);
   /* let fileSize;
    (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024*1024)).toFixed(2) + " MB";*/
      let progressHTML = `<li class="row">
                          <i class="fas fa-file-alt"></i>
                          <div class="content">
                            <div class="details">
                              <span class="name">${fileName}</span>
                              
                            </div>
                           
                          </div>
                        </li>`;
    uploadedArea.classList.add("onprogress");
    progressArea.innerHTML = progressHTML;

  }
}
process.addEventListener("click", () =>{
  let progressHTML = `<li class="row">
                          <i class="fas fa-file-alt"></i>
                          <div class="content">
                            <div class="details">
                              <span class="name">${""}</span>
                              
                            </div>
                           
                          </div>
                        </li>`;
    uploadedArea.classList.add("onprogress");
    progressArea.innerHTML = "";
});

function beforeAfter() {
  document.getElementById('compare').style.width = document.getElementById('slider').value + "%";
}

myfontformName.addEventListener("click", () =>{
  fileInput2.click();
});
var filePath1,myFileName1;
fileInput2.onchange = ({target})=>{
  let file = target.files[0];
  if(file){
    let fileName1 = file.name;
    console.log(fileName1)
    myFileName1=fileName1;
    if(fileName1.length >= 12){
      let splitName = fileName1.split('.');
      fileName1 = splitName[0].substring(0, 13) + "... ." + splitName[1];
    }
    //  let fileLoaded = Math.floor((loaded / total) * 100);
    //let fileTotal = Math.floor(total / 1000);
   /* let fileSize;
    (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024*1024)).toFixed(2) + " MB";*/
      let progressHTML = `<li class="row">
                          <i class="fas fa-file-alt"></i>
                          <div class="content">
                            <div class="details">
                              <span class="name">${fileName1}</span>
                              
                            </div>
                           
                          </div>
                        </li>`;
    uploadedAreaFont.classList.add("onprogress");
    progressAreaFont.innerHTML = progressHTML;
    
  }
}
process_font.addEventListener("click", () =>{
  progressAreaFont.innerHTML = "";
  let progressHTML = `<li class="row">
                          <i class="fas fa-file-alt"></i>
                          <div class="content">
                            <div class="details">
                              <span class="name">${""}</span>
                              
                            </div>
                           
                          </div>
                        </li>`;
  
  uploadedAreaFont.classList.add("onprogress");
  progressAreaFont.innerHTML = "";   
});

process_font_submit.addEventListener("click",()=>{
  let uploadedHTML = `<li class="row">
                        <div class="content upload">
                          <i class="fas fa-file-alt"></i>
                          <div class="details">
                            <span class="name">${myFileName1} • Uploaded</span>
                            
                          </div>
                        </div>
                        <i class="fas fa-check"></i>
                      </li>`;
    uploadedAreaFont.classList.remove("onprogress");
    uploadedAreaFont.insertAdjacentHTML("afterbegin", uploadedHTML);
   alert("Font uploaded successfully!! To check whether your font has been uploaded  check the text highlighted as green")
})

fileInput2.addEventListener("change", stateHandle);

function stateHandle() {
    if (fileInput2.value === "") {
        process_font_submit.disabled = true; //button remains disabled
    } else {
        process_font_submit.disabled = false; //button is enabled
        font_txt.style.display='block'
    }
}