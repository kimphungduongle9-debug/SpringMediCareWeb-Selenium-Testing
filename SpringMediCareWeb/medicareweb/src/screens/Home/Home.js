import { useNavigate } from "react-router-dom";

const Home = () => {
    const nav = useNavigate();

    const featuresData = [
        { title: "Đăng ký tài khoản", desc: "Tạo tài khoản bệnh nhân và quản lý thông tin cá nhân dễ dàng." },
        { title: "Đặt lịch bác sĩ", desc: "Đặt lịch hẹn khám theo bác sĩ và chuyên khoa phù hợp." },
        { title: "Hồ sơ bệnh án", desc: "Lưu trữ, tra cứu lịch sử khám và kết quả xét nghiệm." },
        { title: "Quản lý thuốc", desc: "Theo dõi tồn kho, cảnh báo thuốc sắp hết hoặc gần hết hạn." }
    ];

    const rolesData = [
        { title: "Bệnh nhân", desc: "Đăng ký, đặt lịch, thanh toán, xem đơn thuốc và lịch sử khám." },
        { title: "Bác sĩ", desc: "Quản lý lịch làm việc, cập nhật hồ sơ bệnh án, kê đơn thuốc." },
        { title: "Nhân viên y tế", desc: "Hỗ trợ quản lý khám bệnh, thanh toán và quy trình vận hành." },
        { title: "Quản trị viên", desc: "Quản lý hệ thống, báo cáo thống kê và giám sát hoạt động chung." }
    ];

    return (
        <div className="home-page">
            <section className="hero-wrapper">
                <div className="container">
                    <div className="hero-card">
                        <div className="hero-left">
                            <span className="tag">ĐỀ TÀI 6</span>
                            <h1><b>PHÒNG KHÁM ĐA KHOA TRỰC TUYẾN</b></h1>
                            <p>
                                Hệ thống hỗ trợ bệnh nhân đăng ký khám bệnh trực tuyến, đặt lịch hẹn với bác sĩ, 
                                lưu trữ hồ sơ bệnh án điện tử, quản lý thuốc, thanh toán trực tuyến và thống kê báo cáo hoạt động phòng khám.
                            </p>
                        </div>
                        
                        <div className="hero-right">
                            <div className="info-box">
                                <h3 className="card-title-shared">Mục tiêu hệ thống</h3>
                                <ul>
                                    <li>Đặt lịch khám nhanh chóng</li>
                                    <li>Quản lý hồ sơ bệnh án điện tử</li>
                                    <li>Kê đơn và quản lý thuốc</li>
                                    <li>Thanh toán trực tuyến</li>
                                    <li>Báo cáo thống kê phòng khám</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="main-content">
                <div className="container section-box">
                    <h2 className="card-title-shared">Chức năng nổi bật</h2>
                    <div className="feature-grid">
                        {featuresData.map((item, index) => (
                            <div className="feature-card" key={index}>
                                <h3 className="card-title-shared">{item.title}</h3>
                                <p>{item.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            <section className="main-content" style={{ paddingTop: 0 }}>
                <div className="container section-box">
                    <h2 className="card-title-shared">Đối tượng sử dụng</h2>
                    <div className="role-grid">
                        {rolesData.map((item, index) => (
                            <div className="role-card" key={index}>
                                <h3 className="card-title-shared">{item.title}</h3>
                                <p>{item.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;