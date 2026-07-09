import { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../App.css";
import { MyUserContext } from "../configs/Contexts";

const Header = () => {
  const [user, dispatch] = useContext(MyUserContext);
  const nav = useNavigate();

  const isAdminOrStaff =
    user !== null && (user.role === "admin" || user.role === "staff");
  const isDoctor = user !== null && user.role === "doctor";
  const isPatient = user !== null && user.role === "patient";

  const logout = () => {
    dispatch({
      type: "LOGOUT",
    });

    nav("/login");
  };

  return (
    <header className="topbar">
      <div className="container topbar-inner">
        <div className="logo-area">
          <div className="logo-circle">M</div>
          <div>
            <h1 className="brand-name">MediCare</h1>
            <span className="brand-sub">Phòng khám đa khoa trực tuyến</span>
          </div>
        </div>

        <nav className="main-nav">
          <Link to="/">Trang chủ</Link>

          {(user === null || isPatient || isAdminOrStaff) && (
            <>
              <Link to="/doctor">Bác sĩ</Link>
              <Link to="/specialty">Chuyên khoa</Link>
            </>
          )}

          {isAdminOrStaff && (
            <>
              <Link to="/doctor-schedules">Quản lý lịch làm việc</Link>
              <Link to="/admin-appointments">Quản lý lịch hẹn</Link>
              <div className="nav-dropdown">
                <span className="dropdown-trigger">Quản lý Kho thuốc ▾</span>

                <div className="dropdown-menu-content">
                  <Link to="/admin-drugs">Danh mục thuốc</Link>
                  <Link to="/admin-drugs/statistics">Thống kê thuốc</Link>
                </div>
              </div>

              <Link to="/admin-statistics">Thống kê</Link>
            </>
          )}

          {isDoctor && (
            <>
              <Link to="/doctor-work-schedule">Lịch làm việc của tôi</Link>
              <Link to="/doctor-appointments">Lịch hẹn bệnh nhân</Link>
            </>
          )}

          {isPatient && (
            <>
              <Link to="/my-appointments">Lịch hẹn của tôi</Link>
              <Link to="/patient-medical-history">Lịch sử khám bệnh</Link>
              <Link to="/notifications">Thông báo</Link>
            </>
          )}

          {user === null ? (
            <>
              <Link to="/login">Đăng nhập</Link>
              <Link to="/register" className="btn-nav">
                Đăng ký
              </Link>
            </>
          ) : (
            <>
              <span>Xin chào, {user.firstName}</span>
              <button type="button" className="btn-nav" onClick={logout}>
                Đăng xuất
              </button>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
