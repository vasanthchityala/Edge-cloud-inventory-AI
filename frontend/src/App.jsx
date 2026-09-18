import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowDownToLine,
  ArrowUpRight,
  Boxes,
  CheckCircle2,
  ChevronRight,
  Cloud,
  Database,
  LayoutDashboard,
  Menu,
  Package,
  RefreshCw,
  Search,
  Server,
  Settings,
  ShieldCheck,
  Store,
  TrendingUp,
  Truck,
  XCircle,
  Zap,
} from "lucide-react";

import {
  BarChart,
  Bar,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const API = "http://localhost:8000";

const navGroups = [
  {
    title: "Overview",
    items: [{ id: "dashboard", label: "Dashboard", icon: LayoutDashboard }],
  },
  {
    title: "Operations",
    items: [
      { id: "inventory", label: "Inventory", icon: Boxes },
      { id: "transfers", label: "Transfers", icon: Truck },
    ],
  },
  {
    title: "Intelligence",
    items: [
      { id: "forecasts", label: "Forecasts", icon: TrendingUp },
      { id: "risk", label: "Risk Analysis", icon: AlertTriangle },
      { id: "priority", label: "Priorities", icon: Zap },
      { id: "validation", label: "Validation", icon: ShieldCheck },
    ],
  },
  {
    title: "System",
    items: [{ id: "settings", label: "Settings", icon: Settings }],
  },
];

function App() {
  const [page, setPage] = useState("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [summary, setSummary] = useState(null);
  const [inventory, setInventory] = useState([]);
  const [transfers, setTransfers] = useState([]);
  const [risks, setRisks] = useState([]);
  const [priorities, setPriorities] = useState([]);
  const [validated, setValidated] = useState([]);
  const [forecasts, setForecasts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [backendOnline, setBackendOnline] = useState(false);
  const [search, setSearch] = useState("");

  const loadData = async () => {
    setLoading(true);

    const endpoints = {
      summary: "/dashboard/summary",
      inventory: "/inventory/",
      transfers: "/transfers/",
      risks: "/inventory-risk/",
      priorities: "/unified-priority/",
      validated: "/validated-actions/",
      forecasts: "/forecasts/",
    };

    try {
      const results = await Promise.all(
        Object.entries(endpoints).map(async ([key, endpoint]) => {
          try {
            const response = await fetch(`${API}${endpoint}`);
            if (!response.ok) throw new Error(response.statusText);
            return [key, await response.json()];
          } catch {
            return [key, null];
          }
        })
      );

      const data = Object.fromEntries(results);

      setBackendOnline(Boolean(data.summary));

      if (data.summary) setSummary(data.summary);
      setInventory(normalizeArray(data.inventory));
      setTransfers(normalizeArray(data.transfers));
      setRisks(normalizeArray(data.risks));
      setPriorities(normalizeArray(data.priorities));
      setValidated(normalizeArray(data.validated));
      setForecasts(normalizeArray(data.forecasts));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const filteredInventory = useMemo(() => {
    const query = search.toLowerCase().trim();

    if (!query) return inventory.slice(0, 100);

    return inventory
      .filter((item) =>
        JSON.stringify(item).toLowerCase().includes(query)
      )
      .slice(0, 100);
  }, [inventory, search]);

  const pageTitle = {
    dashboard: "Dashboard",
    inventory: "Inventory",
    transfers: "Transfer Recommendations",
    forecasts: "Demand Forecasts",
    risk: "Inventory Risk Analysis",
    priority: "Unified Priorities",
    validation: "Action Validation",
    settings: "System Settings",
  }[page];

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "" : "collapsed"}`}>
        <div className="brand">
          <div className="brand-mark">
            <Cloud size={22} />
          </div>
          {sidebarOpen && (
            <div>
              <div className="brand-name">EdgeCloud IQ</div>
              <div className="brand-subtitle">Inventory Intelligence</div>
            </div>
          )}
        </div>

        <nav className="navigation">
          {navGroups.map((group) => (
            <div className="nav-group" key={group.title}>
              {sidebarOpen && <div className="nav-heading">{group.title}</div>}

              {group.items.map((item) => {
                const Icon = item.icon;

                return (
                  <button
                    key={item.id}
                    className={`nav-item ${page === item.id ? "active" : ""}`}
                    onClick={() => setPage(item.id)}
                    title={item.label}
                  >
                    <Icon size={18} />
                    {sidebarOpen && <span>{item.label}</span>}
                    {sidebarOpen && page === item.id && (
                      <ChevronRight size={15} className="nav-arrow" />
                    )}
                  </button>
                );
              })}
            </div>
          ))}
        </nav>

        {sidebarOpen && (
          <div className="sidebar-status">
            <div className="status-icon">
              <Activity size={17} />
            </div>
            <div>
              <strong>System status</strong>
              <span>
                <i className={backendOnline ? "online-dot" : "offline-dot"} />
                {backendOnline ? "Backend connected" : "Backend offline"}
              </span>
            </div>
          </div>
        )}
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="topbar-left">
            <button
              className="icon-button"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              <Menu size={20} />
            </button>

            <div>
              <div className="breadcrumb">EdgeCloud IQ / {pageTitle}</div>
              <h1>{pageTitle}</h1>
            </div>
          </div>

          <div className="topbar-actions">
            <div className="connection-pill">
              <span className={backendOnline ? "online-dot" : "offline-dot"} />
              {backendOnline ? "Live" : "Offline"}
            </div>

            <button className="icon-button" onClick={loadData}>
              <RefreshCw size={18} className={loading ? "spin" : ""} />
            </button>

            <div className="avatar">V</div>
          </div>
        </header>

        <div className="page-container">
          {page === "dashboard" && (
            <Dashboard
              summary={summary}
              risks={risks}
              priorities={priorities}
              transfers={transfers}
              validated={validated}
              forecasts={forecasts}
              loading={loading}
              setPage={setPage}
            />
          )}

          {page === "inventory" && (
            <InventoryPage
              inventory={filteredInventory}
              search={search}
              setSearch={setSearch}
              loading={loading}
            />
          )}

          {page === "transfers" && (
            <TransfersPage transfers={transfers} loading={loading} />
          )}

          {page === "forecasts" && (
            <ForecastsPage forecasts={forecasts} loading={loading} />
          )}

          {page === "risk" && (
            <RiskPage risks={risks} loading={loading} />
          )}

          {page === "priority" && (
            <PriorityPage priorities={priorities} loading={loading} />
          )}

          {page === "validation" && (
            <ValidationPage validated={validated} loading={loading} />
          )}

          {page === "settings" && <SettingsPage backendOnline={backendOnline} />}
        </div>
      </main>
    </div>
  );
}

function Dashboard({
  summary,
  risks,
  priorities,
  transfers,
  validated,
  forecasts,
  loading,
  setPage,
}) {
  const riskData = [
    {
      name: "High Risk",
      value: summary?.high_risk_items ?? countLevel(risks, "HIGH"),
    },
    {
      name: "Other",
      value: Math.max(
        0,
        (summary?.total_inventory_risk_records ?? risks.length) -
          (summary?.high_risk_items ?? countLevel(risks, "HIGH"))
      ),
    },
  ];

  const priorityData = ["CRITICAL", "HIGH", "MEDIUM", "LOW"].map((level) => ({
    name: level,
    value:
      summary?.critical_priority_items && level === "CRITICAL"
        ? summary.critical_priority_items
        : countLevel(priorities, level),
  }));

  const actionData = [
    {
      name: "Valid",
      value:
        summary?.valid_actions ??
        countStatus(validated, ["VALID", "APPROVED"]),
    },
    {
      name: "Partial",
      value:
        summary?.partial_actions ?? countStatus(validated, ["PARTIAL"]),
    },
  ];

  return (
    <>
      <section className="welcome-row">
        <div>
          <div className="eyebrow">REAL-TIME INVENTORY INTELLIGENCE</div>
          <h2>Operational overview</h2>
          <p>
            Monitor demand, inventory risk, transfers and validated actions
            across your store network.
          </p>
        </div>

        <div className="network-badge">
          <div className="network-icon">
            <Server size={17} />
          </div>
          <div>
            <span>Network</span>
            <strong>{summary?.total_stores ?? "—"} stores connected</strong>
          </div>
        </div>
      </section>

      <div className="kpi-grid">
        <KpiCard
          icon={Store}
          label="Total Stores"
          value={formatNumber(summary?.total_stores)}
          detail="Active store network"
        />
        <KpiCard
          icon={Package}
          label="Products"
          value={formatNumber(summary?.total_products)}
          detail="Tracked product catalog"
        />
        <KpiCard
          icon={Boxes}
          label="Inventory Records"
          value={formatNumber(summary?.total_inventory_records)}
          detail="Current stock positions"
        />
        <KpiCard
          icon={TrendingUp}
          label="Forecast Records"
          value={formatNumber(summary?.total_forecast_records)}
          detail="Demand intelligence"
        />
        <KpiCard
          icon={AlertTriangle}
          label="High Risk"
          value={formatNumber(summary?.high_risk_items)}
          detail="Requires attention"
          danger
        />
        <KpiCard
          icon={Zap}
          label="Critical Priority"
          value={formatNumber(summary?.critical_priority_items)}
          detail="Highest urgency"
          warning
        />
        <KpiCard
          icon={Truck}
          label="Transfers"
          value={formatNumber(summary?.total_transfers)}
          detail="Recommendations generated"
        />
        <KpiCard
          icon={ShieldCheck}
          label="Validated Actions"
          value={formatNumber(summary?.total_validated_actions)}
          detail="Constraint checked"
        />
      </div>

      <div className="dashboard-grid">
        <Panel
          title="Priority distribution"
          subtitle="Unified edge + cloud intelligence"
          className="large-panel"
        >
          <div className="chart-container">
            {priorities.length || summary ? (
              <ResponsiveContainer width="100%" height={290}>
                <BarChart data={priorityData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                    {priorityData.map((entry) => (
                      <Cell key={entry.name} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState text="No priority data available" />
            )}
          </div>
        </Panel>

        <Panel
          title="Risk exposure"
          subtitle="Current inventory risk profile"
        >
          <div className="donut-wrap">
            <ResponsiveContainer width="100%" height={230}>
              <PieChart>
                <Pie
                  data={riskData}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={65}
                  outerRadius={90}
                  paddingAngle={4}
                >
                  {riskData.map((entry) => (
                    <Cell key={entry.name} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>

            <div className="donut-center">
              <strong>{formatNumber(summary?.high_risk_items)}</strong>
              <span>High risk</span>
            </div>
          </div>

          <div className="legend-list">
            <LegendRow label="High risk items" value={summary?.high_risk_items} />
            <LegendRow
              label="Total risk records"
              value={summary?.total_inventory_risk_records}
            />
          </div>
        </Panel>
      </div>

      <div className="dashboard-grid">
        <Panel
          title="Validated action status"
          subtitle="Final decision layer"
        >
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie
                data={actionData}
                dataKey="value"
                nameKey="name"
                innerRadius={60}
                outerRadius={88}
                paddingAngle={4}
              >
                {actionData.map((entry) => (
                  <Cell key={entry.name} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </Panel>

        <Panel
          title="Intelligence pipeline"
          subtitle="System processing layers"
        >
          <div className="pipeline">
            <PipelineStep
              icon={Store}
              title="Edge Intelligence"
              text="Store-level stock simulation"
              status="Complete"
            />
            <PipelineStep
              icon={Cloud}
              title="Cloud Aggregation"
              text="Cross-store optimization"
              status="Complete"
            />
            <PipelineStep
              icon={Zap}
              title="Unified Priority"
              text="Combined intelligence signals"
              status="Complete"
            />
            <PipelineStep
              icon={ShieldCheck}
              title="Action Validation"
              text="Hard constraint verification"
              status="Complete"
            />
          </div>
        </Panel>
      </div>

      <section className="quick-actions">
        <div>
          <div className="eyebrow">OPERATIONS</div>
          <h3>Explore intelligence</h3>
        </div>

        <div className="action-buttons">
          <button onClick={() => setPage("inventory")}>
            <Boxes size={17} />
            Inventory
            <ChevronRight size={16} />
          </button>
          <button onClick={() => setPage("transfers")}>
            <Truck size={17} />
            Transfers
            <ChevronRight size={16} />
          </button>
          <button onClick={() => setPage("risk")}>
            <AlertTriangle size={17} />
            Risk analysis
            <ChevronRight size={16} />
          </button>
          <button onClick={() => setPage("validation")}>
            <ShieldCheck size={17} />
            Validation
            <ChevronRight size={16} />
          </button>
        </div>
      </section>
    </>
  );
}

function InventoryPage({ inventory, search, setSearch, loading }) {
  return (
    <PageSection
      title="Inventory positions"
      description="Live inventory records retrieved from PostgreSQL."
    >
      <div className="toolbar">
        <div className="search-box">
          <Search size={17} />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search inventory..."
          />
        </div>

        <div className="record-count">
          Showing {inventory.length} records
        </div>
      </div>

      <DataTable
        loading={loading}
        rows={inventory}
        columns={[
          ["id", "ID"],
          ["store_id", "Store"],
          ["product_id", "Product"],
          ["current_stock", "Current Stock"],
          ["safety_stock", "Safety Stock"],
          ["capacity", "Capacity"],
        ]}
      />
    </PageSection>
  );
}

function TransfersPage({ transfers, loading }) {
  return (
    <PageSection
      title="Transfer recommendations"
      description="Optimized inter-store movement generated by the intelligence layer."
    >
      <DataTable
        loading={loading}
        rows={transfers}
        columns={[
          ["id", "ID"],
          ["from_store_id", "From Store"],
          ["to_store_id", "To Store"],
          ["product_id", "Product"],
          ["quantity", "Quantity"],
          ["status", "Status"],
          ["created_at", "Created"],
        ]}
      />
    </PageSection>
  );
}

function ForecastsPage({ forecasts, loading }) {
  const chartData = forecasts.slice(0, 30).map((row, index) => ({
    name: row.forecast_date || `Day ${index + 1}`,
    demand: Number(row.predicted_demand ?? 0),
  }));

  return (
    <PageSection
      title="Demand forecasts"
      description="Predicted demand generated by the forecasting pipeline."
    >
      <Panel title="Forecast trend" subtitle="First available forecast records">
        {chartData.length ? (
          <ResponsiveContainer width="100%" height={330}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" hide />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="demand"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <EmptyState text="No forecast records available" />
        )}
      </Panel>

      <DataTable
        loading={loading}
        rows={forecasts.slice(0, 100)}
        columns={[
          ["id", "ID"],
          ["store_id", "Store"],
          ["product_id", "Product"],
          ["forecast_date", "Date"],
          ["predicted_demand", "Predicted Demand"],
          ["model_version", "Model"],
        ]}
      />
    </PageSection>
  );
}

function RiskPage({ risks, loading }) {
  return (
    <PageSection
      title="Inventory risk"
      description="Identify stock shortages using forecast demand, safety stock and projected inventory."
    >
      <DataTable
        loading={loading}
        rows={risks.slice(0, 100)}
        columns={[
          ["date", "Date"],
          ["store_id", "Store"],
          ["product_id", "Product"],
          ["current_stock", "Stock"],
          ["forecast_demand", "Forecast"],
          ["required_stock", "Required"],
          ["stock_surplus", "Surplus"],
          ["risk_level", "Risk"],
        ]}
        riskColumn="risk_level"
      />
    </PageSection>
  );
}

function PriorityPage({ priorities, loading }) {
  return (
    <PageSection
      title="Unified priorities"
      description="Combined edge-cloud priority signals for operational decision making."
    >
      <DataTable
        loading={loading}
        rows={priorities.slice(0, 100)}
        columns={getDynamicColumns(priorities, [
          "id",
          "store_id",
          "product_id",
          "unified_priority",
          "reason",
        ])}
        priorityColumn="unified_priority"
      />
    </PageSection>
  );
}

function ValidationPage({ validated, loading }) {
  return (
    <PageSection
      title="Validated actions"
      description="Final recommendations after inventory and transfer constraint validation."
    >
      <DataTable
        loading={loading}
        rows={validated.slice(0, 100)}
        columns={[
          ["id", "ID"],
          ["store_id", "Store"],
          ["product_id", "Product"],
          ["action", "Action"],
          ["quantity", "Quantity"],
          ["priority", "Priority"],
          ["validation_status", "Validation"],
          ["remaining_shortage", "Remaining Shortage"],
        ]}
        statusColumn="validation_status"
      />
    </PageSection>
  );
}

function SettingsPage({ backendOnline }) {
  return (
    <PageSection
      title="System settings"
      description="Platform connectivity and environment information."
    >
      <div className="settings-grid">
        <div className="setting-card">
          <Database size={20} />
          <div>
            <span>Database</span>
            <strong>PostgreSQL</strong>
            <small>Connected through FastAPI services</small>
          </div>
          <CheckCircle2 size={19} />
        </div>

        <div className="setting-card">
          <Server size={20} />
          <div>
            <span>Backend API</span>
            <strong>FastAPI</strong>
            <small>http://localhost:8000</small>
          </div>
          {backendOnline ? (
            <CheckCircle2 size={19} />
          ) : (
            <XCircle size={19} />
          )}
        </div>

        <div className="setting-card">
          <Cloud size={20} />
          <div>
            <span>Architecture</span>
            <strong>Edge + Cloud Intelligence</strong>
            <small>Multi-store inventory optimization</small>
          </div>
        </div>
      </div>
    </PageSection>
  );
}

function KpiCard({ icon: Icon, label, value, detail, danger, warning }) {
  return (
    <div className={`kpi-card ${danger ? "danger" : ""} ${warning ? "warning" : ""}`}>
      <div className="kpi-top">
        <div className="kpi-icon">
          <Icon size={18} />
        </div>
        <ArrowUpRight size={16} className="kpi-arrow" />
      </div>
      <div className="kpi-value">{value}</div>
      <div className="kpi-label">{label}</div>
      <div className="kpi-detail">{detail}</div>
    </div>
  );
}

function Panel({ title, subtitle, children, className = "" }) {
  return (
    <div className={`panel ${className}`}>
      <div className="panel-header">
        <div>
          <h3>{title}</h3>
          {subtitle && <p>{subtitle}</p>}
        </div>
      </div>
      {children}
    </div>
  );
}

function PageSection({ title, description, children }) {
  return (
    <div className="content-section">
      <section className="section-heading">
        <div>
          <div className="eyebrow">DATA INTELLIGENCE</div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
      </section>
      {children}
    </div>
  );
}

function DataTable({
  rows,
  columns,
  loading,
  riskColumn,
  priorityColumn,
  statusColumn,
}) {
  if (loading && !rows.length) {
    return (
      <div className="table-card">
        <div className="table-loading">
          <RefreshCw className="spin" size={22} />
          Loading PostgreSQL data...
        </div>
      </div>
    );
  }

  if (!rows.length) {
    return (
      <div className="table-card">
        <EmptyState text="No records available from the backend." />
      </div>
    );
  }

  return (
    <div className="table-card">
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              {columns.map(([key, label]) => (
                <th key={key}>{label}</th>
              ))}
            </tr>
          </thead>

          <tbody>
            {rows.map((row, index) => (
              <tr key={row.id ?? index}>
                {columns.map(([key]) => (
                  <td key={key}>
                    {riskColumn === key ? (
                      <Badge value={row[key]} type="risk" />
                    ) : priorityColumn === key ? (
                      <Badge value={row[key]} type="priority" />
                    ) : statusColumn === key ? (
                      <Badge value={row[key]} type="status" />
                    ) : (
                      formatCell(row[key])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Badge({ value, type }) {
  const normalized = String(value ?? "").toUpperCase();

  let cls = "badge";

  if (normalized.includes("CRITICAL")) cls += " critical";
  else if (normalized.includes("HIGH")) cls += " high";
  else if (normalized.includes("MEDIUM")) cls += " medium";
  else if (normalized.includes("LOW")) cls += " low";
  else if (normalized.includes("VALID")) cls += " valid";
  else if (normalized.includes("PARTIAL")) cls += " partial";
  else cls += " neutral";

  return <span className={cls}>{value ?? "—"}</span>;
}

function PipelineStep({ icon: Icon, title, text, status }) {
  return (
    <div className="pipeline-step">
      <div className="pipeline-icon">
        <Icon size={17} />
      </div>
      <div className="pipeline-text">
        <strong>{title}</strong>
        <span>{text}</span>
      </div>
      <span className="complete">
        <CheckCircle2 size={15} />
        {status}
      </span>
    </div>
  );
}

function LegendRow({ label, value }) {
  return (
    <div className="legend-row">
      <span>{label}</span>
      <strong>{formatNumber(value)}</strong>
    </div>
  );
}

function EmptyState({ text }) {
  return (
    <div className="empty-state">
      <Database size={24} />
      <span>{text}</span>
    </div>
  );
}

function normalizeArray(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.items)) return data.items;
  if (Array.isArray(data?.data)) return data.data;
  if (Array.isArray(data?.results)) return data.results;
  return [];
}

function countLevel(rows, level) {
  return rows.filter(
    (row) =>
      String(
        row.risk_level ?? row.unified_priority ?? row.priority ?? ""
      ).toUpperCase() === level
  ).length;
}

function countStatus(rows, statuses) {
  return rows.filter((row) =>
    statuses.includes(
      String(row.validation_status ?? row.status ?? "").toUpperCase()
    )
  ).length;
}

function getDynamicColumns(rows, preferred) {
  if (!rows.length) {
    return preferred.map((key) => [key, prettify(key)]);
  }

  return preferred
    .filter((key) => rows.some((row) => key in row))
    .map((key) => [key, prettify(key)]);
}

function prettify(value) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatCell(value) {
  if (value === null || value === undefined) return "—";

  if (typeof value === "number") {
    return Number.isInteger(value)
      ? value.toLocaleString()
      : value.toLocaleString(undefined, {
          maximumFractionDigits: 2,
        });
  }

  return String(value);
}

function formatNumber(value) {
  if (value === null || value === undefined) return "—";
  return Number(value).toLocaleString();
}
export default App;

