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
import Loading from "./Loading";

function UploadFile() {
  const [uploadFile, setUploadFile] = useState(null);
  const [labels, setLabels] = useState();
  const [name, setName] = useState("");
  const [scoreBar, setScoreBar] = useState([]);

  const [data, setData] = useState({
    labels: labels,
    datasets: [
      {
        label: name,
        data: scoreBar,
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  });
  const inputFile = useRef(null);
  const updateTemplate = useRef(null);
  const [newCollaboratorModal, setNewCollaboratorModal] = useState(false);
  /* SPINNER LOADING */
  const [loading, setLoading] = useState(false);

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
    e.preventDefault();
    const file = e.target.files[0];
    setUploadFile(file);
    restoreData();
  };

  const submit = async () => {
    try {
      let formData = new FormData();
      formData.append("file", uploadFile);
      setLoading(true);
      setNewCollaboratorModal(true);
      await axios.post("/api/submitFile", formData).then((res) => {
        setName(res.data.name);
        setScoreBar(
          res.data.scoreBar.map((item, index) => {
            let result = (item / 51923.5) * 100;
            return result;
          })
        );

        setLabels(
          res.data.concepts.map((item, index) => {
            return item.value;
          })
        );
        setLoading(false);
        setUploadFile(null);
      });
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

  useEffect(() => {
    setData({
      labels,
      datasets: [
        {
          label: name,
          data: scoreBar,
          backgroundColor: "rgba(255, 99, 132, 0.5)",
        },
      ],
    });
  }, [uploadFile, name, labels, scoreBar]);

  return (
    <>
      <Modal show={newCollaboratorModal} onHide={handleClose} size="lg">
        <div ref={updateTemplate}>
          {loading ? (
            <div className="loading-position">
              <Loading />
            </div>
          ) : (
            <>
              <Form id="formTemplate">
                <Modal.Header closeButton>
                  <Modal.Title>USER SCORE: </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  <Bar options={options} data={data} />
                </Modal.Body>
              </Form>
            </>
          )}
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
              {uploadFile ? <>Ready</> : <>Choose a file</>}{" "}
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
              Cancel
            </span>{" "}
          </span>

          {uploadFile ? (
            <>
              <button type="button" onClick={submit} className="upload-button">
                {" "}
                Run{" "}
              </button>
            </>
          ) : null}

          {name ? (
            <>
              <button
                type="button"
                onClick={() => setNewCollaboratorModal(true)}
                className="upload-button"
              >
                {" "}
                See Graph{" "}
              </button>
            </>
          ) : null}
        </div>
      </form>
    </>
  );
}

export default UploadFile;
