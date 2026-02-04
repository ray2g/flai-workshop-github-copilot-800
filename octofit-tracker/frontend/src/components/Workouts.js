import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Fetching workouts from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="container mt-4">
      <div className="alert alert-info" role="alert">
        <div className="spinner-border spinner-border-sm me-2" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        Loading workouts...
      </div>
    </div>
  );
  
  if (error) return (
    <div className="container mt-4">
      <div className="alert alert-danger" role="alert">
        <strong>Error:</strong> {error}
      </div>
    </div>
  );

  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'beginner': return 'success';
      case 'intermediate': return 'warning';
      case 'advanced': return 'danger';
      default: return 'secondary';
    }
  };

  return (
    <div className="container mt-4">
      <div className="row mb-3">
        <div className="col">
          <h2>💪 Suggested Workouts</h2>
        </div>
        <div className="col-auto">
          <span className="badge bg-info fs-6">{workouts.length} Workouts</span>
        </div>
      </div>
      <div className="row">
        {workouts.length > 0 ? (
          workouts.map(workout => (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body d-flex flex-column">
                  <h5 className="card-title">{workout.name}</h5>
                  <p className="card-text flex-grow-1">{workout.description}</p>
                  <ul className="list-group list-group-flush mt-3">
                    <li className="list-group-item">
                      <strong>Type:</strong> <span className="badge bg-primary ms-2">{workout.workout_type}</span>
                    </li>
                    <li className="list-group-item">
                      <strong>Duration:</strong> {workout.duration} minutes
                    </li>
                    <li className="list-group-item">
                      <strong>Difficulty:</strong> 
                      <span className={`badge bg-${getDifficultyColor(workout.difficulty)} ms-2`}>
                        {workout.difficulty}
                      </span>
                    </li>
                  </ul>
                  <button className="btn btn-primary mt-3 w-100">Start Workout</button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-warning text-center" role="alert">
              <em>No workouts found</em>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Workouts;
