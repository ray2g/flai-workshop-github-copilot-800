import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/users/`;
    console.log('Fetching leaderboard from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard data received:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
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
        Loading leaderboard...
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

  const getMedalEmoji = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  return (
    <div className="container mt-4">
      <div className="text-center mb-4">
        <img 
          src="/celebration.gif" 
          alt="Celebration" 
          style={{width: '400px', height: 'auto', borderRadius: '10px'}}
        />
      </div>
      <div className="row mb-3">
        <div className="col">
          <h2>🏆 Leaderboard</h2>
        </div>
        <div className="col-auto">
          <span className="badge bg-danger fs-6">{leaderboard.length} Competitors</span>
        </div>
      </div>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th scope="col" style={{width: '80px'}}>Rank</th>
              <th scope="col">User</th>
              <th scope="col">Total Calories</th>
              <th scope="col">Total Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length > 0 ? (
              leaderboard.map((entry, index) => {
                const rank = index + 1;
                return (
                  <tr key={entry.id || index} className={rank <= 3 ? 'table-warning' : ''}>
                    <td>
                      <strong style={{fontSize: '1.2rem'}}>{getMedalEmoji(rank)}</strong>
                    </td>
                    <td>
                      <strong>{entry.username || entry.user_name || entry.user}</strong>
                      {entry.first_name && entry.last_name && (
                        <small className="text-muted ms-2">({entry.first_name} {entry.last_name})</small>
                      )}
                    </td>
                    <td>
                      <span className="badge bg-danger">{entry.total_calories_burned || 0} cal</span>
                    </td>
                    <td>
                      <span className="badge bg-success">{entry.total_workouts || 0}</span>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="4" className="text-center py-4">
                  <em>No leaderboard data found</em>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
