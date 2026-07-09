import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { MyUserContext } from "../../configs/Contexts";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import StatisticsTable from "../../components/StatisticsTable";
import StatisticsBarChart from "../../components/StatisticsBarChart";
import StatisticsLineChart from "../../components/StatisticsLineChart";

const AdminStatistics = () => {
  const [user] = useContext(MyUserContext);
  const [totalRevenue, setTotalRevenue] = useState(0);
  const [patientsByGender, setPatientsByGender] = useState([]);
  const [patientsByAgeGroup, setPatientsByAgeGroup] = useState([]);
  const [patientsBySpecialty, setPatientsBySpecialty] = useState([]);
  const [patientsByDiagnosis, setPatientsByDiagnosis] = useState([]);
  const [year, setYear] = useState(new Date().getFullYear());
  const [revenueByMonth, setRevenueByMonth] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const isAdminOrStaff =
    user !== null && (user.role === "admin" || user.role === "staff");

  const loadTotalRevenue = async () => {
    let res = await authApis().get(endpoints.statisticsRevenueTotal);
    setTotalRevenue(res.data);
  };
  const loadPatientsByGender = async () => {
    let res = await authApis().get(endpoints.statisticsPatientsByGender);
    setPatientsByGender(res.data);
  };
  const loadPatientsByAgeGroup = async () => {
    let res = await authApis().get(endpoints.statisticsPatientsByAgeGroup);
    setPatientsByAgeGroup(res.data);
  };
  const loadPatientsBySpecialty = async () => {
    let res = await authApis().get(endpoints.statisticsPatientsBySpecialty);
    setPatientsBySpecialty(res.data);
  };
  const loadPatientsByDiagnosis = async () => {
    let res = await authApis().get(endpoints.statisticsPatientsByDiagnosis);
    setPatientsByDiagnosis(res.data);
  };
  const loadRevenueByMonth = async (selectedYear = year) => {
    let res = await authApis().get(
      endpoints.statisticsRevenueByMonth(selectedYear),
    );
    setRevenueByMonth(res.data);
  };
  const searchRevenueByMonth = async (event) => {
    event.preventDefault();
    setLoading(true);

    try {
      await loadRevenueByMonth(year);
    } catch (err) {
      console.error(err);
      setMsg("Không tải được doanh thu theo tháng.");
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    if (user !== null && isAdminOrStaff) {
      setLoading(true);

      Promise.all([
        loadTotalRevenue(),
        loadPatientsByGender(),
        loadPatientsByAgeGroup(),
        loadPatientsBySpecialty(),
        loadPatientsByDiagnosis(),
        loadRevenueByMonth(),
      ])
        .catch((err) => {
          console.error(err);
          setMsg("Không tải được dữ liệu thống kê.");
        })
        .finally(() => setLoading(false));
    }
  }, [user]);

  if (user === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">
            Vui lòng đăng nhập để sử dụng chức năng này.
          </Alert>
        </div>
      </div>
    );
  }

  if (!isAdminOrStaff) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="danger">
            Bạn không có quyền truy cập trang thống kê.
          </Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Thống kê và báo cáo</h2>
          <p>
            Theo dõi số lượng bệnh nhân, tình hình khám bệnh và doanh thu của
            phòng khám.
          </p>
        </div>

        {msg && <Alert variant="danger">{msg}</Alert>}

        <div className="feature-card">
          <h3>Tổng doanh thu đã thanh toán</h3>
          <p>
            <strong>{Number(totalRevenue).toLocaleString("vi-VN")} VNĐ</strong>
          </p>
        </div>
        <div className="statistics-grid">
          <StatisticsTable
            title="Bệnh nhân theo giới tính"
            headers={["Giới tính", "Số lượng bệnh nhân"]}
            data={patientsByGender}
            emptyMessage="Chưa có dữ liệu bệnh nhân."
            loading={loading}
          >
            <StatisticsBarChart data={patientsByGender} barColor="#7fc8a9" />
          </StatisticsTable>

          <StatisticsTable
            title="Bệnh nhân theo nhóm tuổi"
            headers={["Nhóm tuổi", "Số lượng bệnh nhân"]}
            data={patientsByAgeGroup}
            emptyMessage="Chưa có dữ liệu nhóm tuổi."
            loading={loading}
          >
            <StatisticsBarChart data={patientsByAgeGroup} barColor="#7fc8a9" />
          </StatisticsTable>

          <StatisticsTable
            title="Bệnh nhân theo chuyên khoa"
            headers={["Chuyên khoa", "Số lượng bệnh nhân"]}
            data={patientsBySpecialty}
            emptyMessage="Chưa có dữ liệu chuyên khoa."
            loading={loading}
          >
            <StatisticsBarChart data={patientsBySpecialty} barColor="#7fc8a9" />
          </StatisticsTable>

          <StatisticsTable
            title="Doanh thu theo tháng"
            headers={["Tháng", "Doanh thu đã thanh toán"]}
            data={revenueByMonth}
            emptyMessage="Chưa có doanh thu trong năm này."
            loading={loading}
            renderRow={(item, index) => (
              <tr key={index}>
                <td>Tháng {item[0]}</td>
                <td>{Number(item[1]).toLocaleString("vi-VN")} VNĐ</td>
              </tr>
            )}
          >
            <form
              className="search-form-shared mb-3"
              onSubmit={searchRevenueByMonth}
            >
              <input
                type="number"
                className="search-input-shared"
                value={year}
                onChange={(event) => setYear(event.target.value)}
                placeholder="Nhập năm cần xem"
              />

              <button type="submit" className="btn-main-shared">
                Xem doanh thu
              </button>
            </form>

            <StatisticsLineChart
              data={revenueByMonth}
              valueFormatter={(value) =>
                `${Number(value).toLocaleString("vi-VN")} VNĐ`
              }
            />
          </StatisticsTable>
        </div>

        <StatisticsTable
          title="Bệnh phổ biến trong cộng đồng"
          headers={["Chẩn đoán", "Số lượng bệnh nhân"]}
          data={patientsByDiagnosis}
          emptyMessage="Chưa có dữ liệu chẩn đoán."
          loading={loading}
          className="diagnosis-statistics-card"
        />

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default AdminStatistics;
