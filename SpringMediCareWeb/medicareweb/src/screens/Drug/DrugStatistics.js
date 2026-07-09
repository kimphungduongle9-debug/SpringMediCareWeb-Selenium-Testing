import { useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import StatisticsTable from "../../components/StatisticsTable";
import StatisticsBarChart from "../../components/StatisticsBarChart";

const DrugStatistics = () => {
  const [drugStatistics, setDrugStatistics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const loadDrugStatistics = async () => {
    const res = await authApis().get(
      endpoints.statisticsDrugsByCategory
    );

    setDrugStatistics(res.data);
  };

  useEffect(() => {
    setLoading(true);

    loadDrugStatistics()
      .catch((err) => {
        console.error(err);
        setMsg("Không tải được dữ liệu thống kê thuốc.");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Thống kê thuốc</h2>
          <p>Theo dõi số lượng thuốc theo từng danh mục.</p>
        </div>

        {msg && <Alert variant="danger">{msg}</Alert>}

        <StatisticsTable
          title="Thuốc theo danh mục"
          headers={["Danh mục thuốc", "Số lượng"]}
          data={drugStatistics}
          emptyMessage="Chưa có dữ liệu thuốc."
          loading={loading}
        >
          <StatisticsBarChart
            data={drugStatistics}
            barColor="#7fc8a9"
          />
        </StatisticsTable>

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default DrugStatistics;