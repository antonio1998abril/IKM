import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { Modal, Form, Button } from "react-bootstrap";
import { Bar, PolarArea } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  ArcElement,
} from "chart.js";
import Loading from "./Loading";

function UploadFile() {
  const [uploadFile, setUploadFile] = useState(null);
  /* 📝 Add labels to each bar */
  /* Bar */
  const [labels, setLabels] = useState();
  const [scoreBar, setScoreBar] = useState([]);
  /* Circle */
  const [scoreBarCircle, setScoreBarCircle] = useState([]);
  /* Data Miner */
  const [dataMiner,setDataMiner] = useState({
    "Assessment Result for":"",
    "ID":"", 
    "Date":"",
    "Subject":"",
    "Client":"",
    "Score":0,
    "Percentile":0,
    "Subject Coverage":0,
    
  });
  const [name, setName] = useState("");
  /* Footer Level */
  const [footerLevel,setFooterLevel] = useState([
    {label: '', context: 'Work Speed/Accuracy'},
    {label: '', context: 'Application Ability'}
  ]);
  /* Set data for Bar graph */
  const [data, setData] = useState({
    labels: labels,
    datasets: [
      {
        label: "Subject Analysis",
        data: scoreBar,
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  });

  /* Set data for  Circle graph */
  const [dataCircle, setDataCircle] = useState({
    labels: ["None"],
    datasets: [
      {
        label: {"Subject Coverage":dataMiner["Subject Coverage"]},
        data: scoreBarCircle,
        backgroundColor: ["rgba(224, 0, 25, 0.8)"],
      },
    ],
  });

  const inputFile = useRef(null);
  const updateTemplate = useRef(null);
  const [newCollaboratorModal, setNewCollaboratorModal] = useState(false);
  /* SPINNER LOADING */
  const [loading, setLoading] = useState(false);
  /* 🔥🔥 Graph Configurations 🔥🔥 */
  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    RadialLinearScale,
    ArcElement
  );

  const optionsBar = {
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

  const optionsArea = {
    type: "polarArea",
    data: dataCircle,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Subject Coverage",
        },
      },
    },
  };
  /* 🔥🔥 Graph Configurations 🔥🔥*/

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
        console.log(res.data);
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

        /* CIRCLE GRAPH */

        let valuesCircle = [];
        res.data.subjectCoverage.map((item, index) => {
          return valuesCircle.push(item.value);
        });
        valuesCircle = valuesCircle.filter((item) => item !== 0);
        setScoreBarCircle(valuesCircle);

        /* Data Miner */

     
      
        let object = res.data.dataMiner.reduce((obj, item) => (obj[item.label] = item.value, obj) ,{});
        setDataMiner(object)
        setFooterLevel(res.data.FooterLevel)
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
    /* Set default BarGraph */
    setData({
      labels,
      datasets: [
        {
          label: "Subject Analysis",
          data: scoreBar,
          backgroundColor: "rgba(255, 99, 132, 0.5)",
        },
      ],
    });

    {
      scoreBarCircle.length === 3
        ? setDataCircle({
            labels: ["Week", "Proficient", "Strong"],
            datasets: [
              {
                label: `Subject Coverage, ${dataMiner["Subject Coverage"]}, This area`,
                data: scoreBarCircle,

                backgroundColor: [
                  "rgba(224, 0, 25, 0.8)",
                  "rgba(253, 156, 12, 0.8)",
                  "rgba(2, 194, 68, 0.8)",
                ],
              },
            ],
          })
        : setDataCircle({
            labels: ["Week", "Proficient"],
            datasets: [
              {
                label:`Subject Coverage: ${dataMiner["Subject Coverage"]},This area`,
                data: scoreBarCircle,

                backgroundColor: [
                  "rgba(224, 0, 25, 0.8)",
                  "rgba(253, 156, 12, 0.8)",
                ],
              },
            ],
          });
    }
  }, [uploadFile, name, labels, scoreBar, scoreBarCircle,dataMiner]);
 

  console.log("data",footerLevel)

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
                  <h6>Client: {dataMiner.Client}, Date: {dataMiner.Date}, Subject: {dataMiner.Subject}</h6>
                  <h6>ID: {dataMiner.ID}. </h6>
                  <h6>Name: {name}, Score: {dataMiner.Score}.</h6>
                  <h6>Percentile: {dataMiner.Percentile}.</h6>
                  <Bar options={optionsBar} data={data}/>

                
                  <div>
                  Work Speed/Accuracy: <h6 className="text-primary">{footerLevel[0].label}</h6>
                  </div>
                  <div>
                  Application Ability : <h6 className="text-primary">{footerLevel[1].label}</h6>
                  </div>

                  <PolarArea options={optionsArea} data={dataCircle} />

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
