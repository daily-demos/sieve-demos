import { SyntheticEvent, useEffect, useRef, useState } from "react";

const apiURL = 'http://127.0.0.1:5000';

type Project = {
  name: string,
  project_id: string,
  status?: ProjectStatus,
  downloadLink?: string,
}

type ProjectStatus = 'Not started' | 'In progress' | 'Succeeded' | 'Failed'

function App() {
  
  function render() {
    return(
    <div>
      <h1>Upload file</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleChange}/>
        <button>Upload</button>
      </form>
      <hr />
      {project &&
        <div className="flex gap-8">
          <div>{project.name}</div>
          <div>{project.project_id}</div>
          <div>{project.status}</div>
          {project.downloadLink &&
            <div><a href={project.downloadLink} className="text-blue-600">Download</a></div>
          }
        </div>
      }
    </div>
    )
  }

  const [file, setFile] = useState()
  const [project, setProject] = useState<Project>({ project_id: '0', name: ''});
  const [timer, setTimer] = useState<number>(0)

  useEffect(() => {
    if (project?.status === 'Succeeded') clearInterval(timer)
  }, [project?.status])

  function handleChange(event: any) {
    setFile(event.target.files[0])
  }

  function handleSubmit(event: SyntheticEvent) {
    event.preventDefault();
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', file.name);
    fetch(`${apiURL}/upload`, { method: 'POST', body: formData })
      .then((res) => {
        if (res.ok === false) {
          throw Error(`upload request failed: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        const {name} = data;
        console.log(name)
        // const { name, project_id } = data;
        // const proj:Project = {name, project_id, status: 'Not started'}
        // setProject(proj);

        // const t = setInterval(() => {
        //   checkStatus(proj)
        // }, 2000);
        // setTimer(t);
      })
      .catch((e) => {
        console.error('Failed to process uploaded video:', e);
      });
  }

  function checkStatus(project: Project, recordingID = null) {
      fetch(`${apiURL}/projects/${project.project_id}`)
        .then((res) => {
          if (!res.ok) {
            throw Error(`status request failed: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          const { status } = data;
        
          if (status === 'Succeeded') {
            setProject({...project, status, downloadLink: `${apiURL}/projects/${project.project_id}/download`})
          } else {
            setProject({...project, status})
          }
        })
        .catch((err) => {
          console.error('failed to check project status: ', err);
          checkStatus(project, recordingID);
        });
  }
  

  return render();
}



export default App
