import React, { useEffect, useRef, useState } from "react";
import axios from "axios";

function UploadFile() {
  const [uploadFile, setUploadFile] = useState(null);
  const [data,setData] = useState([])
  const inputFile = useRef(null);

  const onButtonClick = (e) => {
    // `current` points to the mounted file input element
    /* inputFile.current.click();
   setUploadFile(inputFile.current.value)
   */
   restoreData()
    e.preventDefault();
    const file = e.target.files[0];
    setUploadFile(file);
  };

  const submit = async () => {
    try {
      let formData = new FormData();
      formData.append("file", uploadFile)
      const res = await axios.post("/api/submitFile",formData)
      setData(res.data.message)
     

    } catch (err) {
      console.log(err);
    }
  };

  const restoreData = async()=> {
      await axios.delete("/api/deleteFile")
  }

  useEffect(() => {}, [uploadFile,data]);
  console.log(data)
  return (
    <>
      <form className="form-container" encType="multipart/form-data">
        <div className="upload-files-container">


         
          <div className="drag-file-area">
            <span className="material-icons-outlined upload-icon" type="submit">
              {" "}
              {uploadFile ? <>Done</> : <>File_upload</>}{" "}
            </span>
            <input
              type="file"
              id="file"
              name="file"
              /* ref={inputFile} */ /* style={{display: 'none'}} */ ref={
                inputFile
              }
              onChange={onButtonClick}
            />

            {/* 	<h3 className="dynamic-message"> Drag & drop any file here </h3> */}
            {/* 	<label className="label"> or <span className="browse-files"> <input type="file" className="default-file-input"/> <span className="browse-files-text">browse file</span> <span>from device</span> </span> </label> */}
          </div>
          <span className="cannot-upload-message">
            {" "}
            <span className="material-icons-outlined">error</span> Please select
            a file first{" "}
            <span className="material-icons-outlined cancel-alert-button">
              cancel
            </span>{" "}
          </span>
          {/* <div className="file-block">
			<div className="file-info"> <span className="material-icons-outlined file-icon">description</span> <span className="file-name"> </span> | <span className="file-size">  </span> </div>
			<span className="material-icons remove-file-icon">delete</span>
			<div className="progress-bar"> </div>
		</div> */}
          <button type="button" onClick={submit} className="upload-button">
            {" "}
            Get Values{" "}
          </button>

 
        </div>
      </form>
    </>
  );
}

export default UploadFile;
