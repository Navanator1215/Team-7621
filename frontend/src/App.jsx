import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

const emptyForm = {
  crop: "",
  variety: "",
  location: "",
  objective: "",
  season: "",
  status: "Active",
  notes: "",
};

export default function App(){
  const [trails, setTrials] = useState([]);
  const [from, setForm] = useState(emptyForm);
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(null);
  const [error, setError] = useState("");
  const [filtertext, setFilterText] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [editingId, setEditingId] = useState(null);

  const fetchTrails = async () => {
    try{
      setLoading(true);
      const res = await fetch(`${API_BASE}/trials`);
      if(!res.ok){
        throw new Error("Failed to load trails.")
      }
      const data = await res.json();
      setTrials(data);
    } catch(err){
      setError(err.message || "Something went wrong!")
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrails();
  }, []);

  const handleChange = (e) => {
    const {name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value}));
  };

  const resetForm = () => {
    setForm(emptyForm);
    setSelectedFile(null);
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      if (editingId) {
        const res = await fetch(`${API_BASE}/trials/${editingId}`, {
          method: "PUT",
          headers: {"Content-Type": "application/json" },
          body: JSON.stringify(form),
        });

        if(!res.ok) {
          throw new Error("Failed to upload trial.");
        }
      } else {
        const formData = new FormData();
        Object.entries(form).forEach(([key, value]) => {
          formData.append(key, value);
        });

        if (selectedFile) {
          formData.append("media", selectedFile);
        }

        const res = await fetch(`${API_BASE}/trials`, {
          method: "POST",
          body: formData,
        });

        if (!res.ok) {
          const data = await res.json();
          throw new Error(data.error || "Failed to create trial" )
        }
      }

      resetForm();
      fetchTrails();
    } catch (err) {
      setError(err.message || "Something went wrong");
    }
  };

  const handleEdit = (trial) => {
    setEditingId(trial.id);
    setForm({
      crop: trial.crop || "",
      variety: trial.variety || "",
      location: trial.location || "",
      objective: trial.objective || "",
      season: trial.season || "",
      status: trial.status || "Active",
      notes: trial.notes || "",
    });
    setSelectedFile(null);
  };

  const handleDelete = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/trials/${id}`, {
        method: "DELETE",
      });

      if (!res.ok) {
        throw new Error("Failed to delete trial");
      }

      fetchTrials();
    } catch (err) {
      setError(err.message || "Something went wrong");
    }
  };

  const filteredTrials = useMemo(() => {
    return trials.filter((trial) => {
      const matchesText = [trial.crop, trial.variety, trial.location, trial.objective]
        .join(" ")
        .toLowerCase()
        .includes(filterText.toLowerCase());

      const matchesStatus =
        statusFilter === "All" || trial.status === statusFilter;

      return matchesText && matchesStatus;
    });
  }, [trials, filterText, statusFilter]);

  const summary = useMemo(() => {
    const total = trials.length;
    const active = trials.filter((t) => t.status === "Active").length;
    const completed = trials.filter((t) => t.status === "Completed").length;
    const locations = new Set(trials.map((t) => t.location).filter(Boolean)).size;

    return { total, active, completed, locations };
  }, [trials]);

  return (
    <div className="app">
      <h1>Agri R&D Dashboard</h1>
      <p className="subtitle">Manage and review agricultural field trials</p>

      {error && <p className="error">{error}</p>}
      {loading && <p>Loading...</p>}

      <div className="summary-grid">
        <div className="summary-card">
          <h3>Total Trials</h3>
          <p>{summary.total}</p>
        </div>
        <div className="summary-card">
          <h3>Active</h3>
          <p>{summary.active}</p>
        </div>
        <div className="summary-card">
          <h3>Completed</h3>
          <p>{summary.completed}</p>
        </div>
        <div className="summary-card">
          <h3>Locations</h3>
          <p>{summary.locations}</p>
        </div>
      </div>

      <section className="card">
        <h2>{editingId ? "Edit Trial" : "Create Trial"}</h2>
        <form className="rd-form" onSubmit={handleSubmit}>
          <input name="crop" placeholder="Crop" value={form.crop} onChange={handleChange} required />
          <input name="variety" placeholder="Variety" value={form.variety} onChange={handleChange} />
          <input name="location" placeholder="Location" value={form.location} onChange={handleChange} required />
          <input name="objective" placeholder="Objective" value={form.objective} onChange={handleChange} />
          <input name="season" placeholder="Season" value={form.season} onChange={handleChange} />
          <select name="status" value={form.status} onChange={handleChange}>
            <option value="Active">Active</option>
            <option value="Completed">Completed</option>
            <option value="Planned">Planned</option>
          </select>
          <textarea
            name="notes"
            placeholder="Notes"
            value={form.notes}
            onChange={handleChange}
            style={{ gridColumn: "1 / -1" }}
          />

          {!editingId && (
            <input
              type="file"
              accept="image/*,video/*"
              onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
              style={{ gridColumn: "1 / -1" }}
            />
          )}
          <button type="submit">{editingId ? "Update Trial" : "Add Trial"}</button>
          {editingId && (
            <button type="button" className="cancel-btn" onClick={resetForm}>
              Cancel
            </button>
          )}
        </form>
      </section>

      <section className="card">
        <div className="trials-header">
          <h2>Field Trials</h2>
          <div className="filter-bar">
            <input
              placeholder="Search crop, variety, location..."
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
            />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="All">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Completed">Completed</option>
              <option value="Planned">Planned</option>
            </select>
          </div>
        </div>

        <table>
          <thead>
            <tr>
              <th>Crop</th>
              <th>Variety</th>
              <th>Location</th>
              <th>Status</th>
              <th>Media</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredTrials.map((trial) => (
              <tr key={trial.id}>
                <td>{trial.crop}</td>
                <td>{trial.variety || "-"}</td>
                <td>{trial.location}</td>
                <td>{trial.status}</td>
                <td>
                  {trial.media_type === "image" && trial.media_url && (
                    <img
                      src={trial.media_url}
                      alt={trial.crop}
                      style={{ width: "100px", borderRadius: "10px" }}
                    />
                  )}
                  {trial.media_type === "video" && trial.media_url && (
                    <video width="140" controls>
                      <source src={trial.media_url} />
                      Your browser does not support video.
                    </video>
                  )}
                  {!trial.media_url && "No media"}
                </td>
                <td className="actions-cell">
                  <button className="edit-btn" onClick={() => handleEdit(trial)}>
                    Edit
                  </button>
                  <button className="delete-btn" onClick={() => handleDelete(trial.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
