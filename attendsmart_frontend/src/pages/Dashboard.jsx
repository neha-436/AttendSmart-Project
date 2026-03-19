import { useEffect, useState } from "react"

function Dashboard() {

  const [subjects, setSubjects] = useState([])

  useEffect(() => {
    fetch("http://127.0.0.1:8000/subjects")
      .then(res => res.json())
      .then(data => {
        setSubjects(data)
      })
  }, [])

  return (
    <div>
      <h1>AttendSmart Dashboard</h1>

      <h2>Your Subjects</h2>

      <ul>
        {subjects.map((subject) => (
          <li key={subject.id}>{subject.name}</li>
        ))}
      </ul>

    </div>
  )
}

export default Dashboard