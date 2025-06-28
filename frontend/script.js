// ===============================
// START MATCH (index.html)
// ===============================
if (document.getElementById("startForm")) {
  document.getElementById("startForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const player1 = document.getElementById("player1").value;
    const player2 = document.getElementById("player2").value;

    const res = await fetch("http://127.0.0.1:5000/start_match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ player1, player2, match_id: 1 })
    });

    const data = await res.json();
    if (data.match_id) {
      localStorage.setItem("match_id", data.match_id);
      localStorage.setItem("player1", player1);
      localStorage.setItem("player2", player2);
      window.location.href = "match.html";
    } else {
      document.getElementById("matchStatus").textContent = data.error || "Failed to start match";
    }
  });
}

//
// ===============================
// MATCH LOGIC (match.html)
// ===============================
if (window.location.pathname.includes("match.html")) {
  const matchId = localStorage.getItem("match_id");
  const player1 = localStorage.getItem("player1");
  const player2 = localStorage.getItem("player2");

  document.getElementById("matchIdDisplay").textContent = matchId;
  document.getElementById("p1Name").textContent = player1;
  document.getElementById("p2Name").textContent = player2;
  document.getElementById("p1Hp").textContent = "100";
  document.getElementById("p2Hp").textContent = "100";

  // Update HP bar % width
  function updateHpBar(player, hpValue) {
    const bar = document.getElementById(`${player}Bar`);
    const percentage = Math.max(0, Math.min(hpValue, 100));
    bar.style.width = `${percentage}%`;
    if (percentage <= 50 && percentage > 20) {
      bar.style.backgroundColor = "orange";
    } else if (percentage <= 20) {
      bar.style.backgroundColor = "red";
    } else {
      bar.style.backgroundColor = "green";
    }
  }

  // Initial bar setup
  updateHpBar("p1", 100);
  updateHpBar("p2", 100);

  window.attack = async function (targetPlayer) {
    const res = await fetch("http://127.0.0.1:5000/update_health", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        match_id: matchId,
        player: targetPlayer,
        damage: 10
      })
    });

    const data = await res.json();

    if (data.status === "health updated") {
      const updatedHp = data[`${targetPlayer}_hp`];
      document.getElementById(`${targetPlayer}Hp`).textContent = updatedHp;
      updateHpBar(targetPlayer, parseInt(updatedHp));
      document.getElementById("actionStatus").textContent = `Attack successful!`;

      if (updatedHp <= 0) {
        const winner = targetPlayer === "p1" ? player2 : player1;
        const loser = targetPlayer === "p1" ? player1 : player2;

        localStorage.setItem("winner", winner);
        localStorage.setItem("loser", loser);

        alert(`${loser} has been defeated! Click 'End Match' to finish.`);

        document.querySelectorAll("button").forEach(btn => {
          if (btn.textContent.includes("Attack")) {
            btn.disabled = true;
          }
        });
      }
    } else {
      document.getElementById("actionStatus").textContent = data.error || "Attack failed";
    }
  };

  window.endMatch = async function () {
    const winner = localStorage.getItem("winner");
    const loser = localStorage.getItem("loser");

    if (!winner || !loser) {
      alert("Match not finished. One player must reach 0 HP first.");
      return;
    }

    const res = await fetch("http://127.0.0.1:5000/end_match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        match_id: matchId,
        winner,
        loser
      })
    });

    const data = await res.json();
    document.getElementById("resultMsg").textContent = data.status || data.error || "Match ended.";

    // Store player names in a temporary variable
    const tempPlayers = {
      player1: localStorage.getItem("player1"),
      player2: localStorage.getItem("player2")
    };

    localStorage.clear();

    // Restore player names if they exist
    if (tempPlayers.player1 && tempPlayers.player2) {
      localStorage.setItem("player1", tempPlayers.player1);
      localStorage.setItem("player2", tempPlayers.player2);
    }

    setTimeout(() => {
      window.location.href = "leaderboard.html";
    }, 2000);
  };
}

//
// ===============================
// LEADERBOARD (leaderboard.html)
// ===============================
if (window.location.pathname.includes("leaderboard.html")) {
  fetch("http://127.0.0.1:5000/leaderboard")
    .then(res => res.json())
    .then(data => {
      const body = document.getElementById("leaderboardBody");
      body.innerHTML = "";

      if (data.leaderboard.length === 0) {
        body.innerHTML = "<tr><td colspan='3'>No players yet.</td></tr>";
        return;
      }

      data.leaderboard.forEach((entry, index) => {
        const [player, score] = entry;
        const row = `<tr>
          <td>${index + 1}</td>
          <td>${player.replace("player:", "")}</td>
          <td>${score}</td>
        </tr>`;
        body.innerHTML += row;
      });
    })
    .catch(() => {
      document.getElementById("leaderboardBody").innerHTML =
        `<tr><td colspan="3">Failed to load leaderboard</td></tr>`;
    });

  // Buttons work here
  window.restartSameMatch = async function () {
    const player1 = localStorage.getItem("player1");
    const player2 = localStorage.getItem("player2");
  
    if (!player1 || !player2) {
      alert("No previous match found. Start a new one.");
      return;
    }
  
    // Request a fresh match from the backend
    const res = await fetch("http://127.0.0.1:5000/start_match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        player1, 
        player2,
        match_id: null  // Let backend generate new match_id
      })
    });
  
    const data = await res.json();
  
    if (data.match_id) {
      localStorage.setItem("match_id", data.match_id);
      window.location.href = "match.html";
    } else {
      alert(data.error || "Failed to start match");
    }
  };

  window.startNewMatch = function() {
    localStorage.clear();  // Clear all stored data
    window.location.href = "index.html";  // Redirect to start page
  };
}
