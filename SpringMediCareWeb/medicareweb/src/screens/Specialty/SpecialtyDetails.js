import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Alert } from "react-bootstrap";
import MySpinner from "../../components/MySpinner";
import Apis, { endpoints } from "../../configs/Apis";

const SpecialtyDetails = () => {
    const { specialtyId } = useParams();
    const [specialty, setSpecialty] = useState(null);
    const [specialtyDoctors, setSpecialtyDoctors] = useState([]);
    const [loading, setLoading] = useState(false);
    const nav = useNavigate();

    const loadSpecialtyDetails = async () => {
        try {
            setLoading(true);

            let urlSpecialty = `${endpoints['specialties']}/${specialtyId}`;
            let resSpecialty = await Apis.get(urlSpecialty);
            setSpecialty(resSpecialty.data);

            let urlDoctors = `${endpoints['doctors']}?specialtyId=${specialtyId}`;
            let resDoctors = await Apis.get(urlDoctors);
            setSpecialtyDoctors(resDoctors.data);

        } catch (ex) {
            console.error("Lỗi khi tải chi tiết chuyên khoa:", ex);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (specialtyId) {
            loadSpecialtyDetails();
        }

    }, [specialtyId]);

    const handleBooking = (doctorId) => {
        nav(`/booking?doctorId=${doctorId}`);
    }
    if (loading) {
        return (
            <div style={{ textAlign: "center", marginTop: "40px" }}>
                <MySpinner />
            </div>
        );
    }

    if (!specialty && !loading) {
        return (
            <div className="container mt-4">
                <Alert variant="danger" className="text-center">
                    Không tìm thấy thông tin chuyên khoa yêu cầu!
                </Alert>
            </div>
        );
    }

    return (
        <div className="main-content">
            <div className="container">
                
                <div className="section-box" style={{ textAlign: "center" }}>
                    <h2>Chuyên khoa: {specialty.name}</h2>
                    <p style={{ color: "red", fontWeight: "bold", marginTop: "10px" }}>
                        Số lượng bác sĩ đang công tác: <span>{specialtyDoctors.length}</span> bác sĩ
                    </p>
                </div>

                <div className="feature-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))" }}>
                    

                    <div className="feature-card">
                        <img 
                            className="specialty-img" 
                            src={specialty.image || "https://via.placeholder.com/300x220?text=Chuyen+Khoa"} 
                            alt={specialty.name} 
                            style={{ height: "300px", objectFit: "cover" }}
                        />
                    </div>

                    <div className="feature-card" style={{ justifyContent: "space-between" }}>
                        <div>
                            <h3 className="card-title-shared">
                                <strong>Thông tin giới thiệu</strong>
                            </h3>
                            <p className="card-text-shared" style={{ fontSize: "16px", lineHeight: "1.6" }}>
                                {specialty.description || "Chưa có mô tả chi tiết cho chuyên khoa này."}
                            </p>
                        </div>
                    </div>

                </div>

                <div className="section-box" style={{ marginTop: "50px" }}>
                    <h2 style={{ textAlign: "center" }}>Đội ngũ bác sĩ trực thuộc</h2>
                </div>

                {specialtyDoctors.length === 0 ? (
                    <Alert variant="warning" className="mt-2">
                        Hiện chưa có bác sĩ nào thuộc chuyên khoa này.
                    </Alert>
                ) : (
                    <div className="feature-grid">
                        {specialtyDoctors.map(d => (
                            <div className="feature-card" key={d.doctorId}>
                                <img 
                                    className="specialty-img" 
                                    src={d.image || "https://via.placeholder.com/300x220?text=Bac+Si"} 
                                    alt={d.fullName} 
                                    style={{ height: "200px", objectFit: "cover" }}
                                />
                                
                                <h3 className="card-title-shared">
                                    <strong>{d.fullName}</strong>
                                </h3>
                                
                                <p className="card-text-shared">
                                    Kinh nghiệm: {d.experienceYears} năm trong nghề.
                                </p>
                                
                                <div className="card-actions-shared">
                                    <button onClick={() => handleBooking(d.doctorId)} className="btn-action-shared">
                                        Đặt lịch hẹn
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                <div style={{ textAlign: "center", marginTop: "50px", marginBottom: "20px" }}>
                    <button 
                        className="btn-outline-shared" 
                        onClick={() => nav("/specialty")} 
                        style={{ height: "45px", padding: "0 40px", fontWeight: "bold" }}
                    >
                        ⬅️ Quay lại danh mục chuyên khoa
                    </button>
                </div>

            </div>
        </div>
    );
};

export default SpecialtyDetails;