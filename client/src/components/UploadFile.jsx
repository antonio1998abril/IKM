import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { Modal, Form, Button } from "react-bootstrap";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

function UploadFile() {
  const [uploadFile, setUploadFile] = useState(null);
  const labels = [
    "Spring Boot Testing",
    "IOC Container",
    "REST Web Services",
    "Exception Handling",
    "Generics and Collections",
    "Object Orientation in Java",
    "Design Patterns",
    "Spring Boot Restful",
    "Lambda Expressions",
    "Java Streams",
    "Cloud Fundamentals",
    "Spring: Reactive Programming",
    "Managing Entities in Java Persistence",
    "Concurrency",
    "Agile Concepts",
    "Understanding Microservices",
  ];

  const [data, setData] = useState({
    labels,
    datasets: [
      {
        label: "Josh",
        data: [],
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  });
  const inputFile = useRef(null);
  const updateTemplate = useRef(null);
  const [newCollaboratorModal, setNewCollaboratorModal] = useState(false);

  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Result:",
      },
    },
  };

  const onButtonClick = (e) => {
    // `current` points to the mounted file input element
    /* inputFile.current.click();
   setUploadFile(inputFile.current.value)
   */
    restoreData();
    e.preventDefault();
    const file = e.target.files[0];
    setUploadFile(file);
  };

  const submit = async () => {
    try {
      /*  let formData = new FormData();
      formData.append("file", uploadFile); */

      /*     const convert = async () => {
        restoreData();
        const arr = new Uint8Array(uploadFile)
        let blob = new Blob([arr],{type:'application/pdf'})
        let name = "data.pdf"
         let newFile = new File([blob],name,{
          type:blob.type
         })
    
        let formData = new FormData();
        formData.append("file", newFile);
        
        const res = await axios.post("/api/convert", formData);
       
      }; */

      /*       const arr = new Uint8Array(uploadFile)
        let blob = new Blob([arr],{type:'application/docx'})
        let name = "data.docx"
         let newFile = new File([blob],name,{
          type:blob.type
         })
     */
      let formData = new FormData();
      formData.append("file", uploadFile);

      const res = await axios.post("/api/submitFile", formData);
      const size = res.data.message.map((item, index) => {
        let size = [];
        let result = ( item / 2000 ) * 100
        size.push(result);
        return size;
      });

      setData({
        labels,
        datasets: [
          {
            label: "Dataset 1",
            data: size,
            backgroundColor: "rgba(255, 99, 132, 0.5)",
          },
        ],
      });
      setNewCollaboratorModal(true);
    } catch (err) {
      console.log(err);
    }
  };

  const restoreData = async () => {
    await axios.delete("/api/deleteFile");
  };

  const handleClose = () => {
    setNewCollaboratorModal(false);
  };

  useEffect(() => {}, [uploadFile, data]);
  console.log(data);
  return (
    <>
      <Modal show={newCollaboratorModal} onHide={handleClose} size="lg">
        <div ref={updateTemplate}>
          <Form id="formTemplate">
            <Modal.Header closeButton>
              <Modal.Title>USER STATUS</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Bar options={options} data={data} />;
            </Modal.Body>
          </Form>
        </div>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

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
          <button
            type="button"
            onClick={() => setNewCollaboratorModal(true)}
            className="upload-button"
          >
            {" "}
            See Graph{" "}
          </button>
        </div>
      </form>
    </>
  );
}

export default UploadFile;
