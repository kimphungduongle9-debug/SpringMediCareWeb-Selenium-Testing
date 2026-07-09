import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Alert } from "react-bootstrap";
import MySpinner from "../../components/MySpinner";
import Apis, { endpoints } from "../../configs/Apis";

const DoctorBySpecialty = () => {

    const { specialtyId } = useParams();
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(false);
    const [specialtyName, setSpecialtyName] = useState("");
    const nav = useNavigate();
    

    const loadDoctorsOfSpecialty = async () => {
        try {
            setLoading(true);

            let url = `${endpoints['doctors']}?specialtyId=${specialtyId}`;
            let res = await Apis.get(url);
            setDoctors(res.data);

            let urlSpecialty = `${endpoints['specialties']}/${specialtyId}`; 
            let resSpecialty = await Apis.get(urlSpecialty);
            setSpecialtyName(resSpecialty.data.name);
        } catch (ex) {
            console.error("Lỗi khi tải bác sĩ theo khoa:", ex);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (specialtyId) {
            loadDoctorsOfSpecialty();
        }
    }, [specialtyId]);

    const handleBooking = (doctorId) => {
        nav(`/booking?doctorId=${doctorId}`);
    }
    return (
        <div className="main-content">
            <div className="container">
                
                <div className="section-box" style={{ textAlign: "center", marginBottom: "30px" }}>
                    <h2 card-title-shared>Bác sĩ thuộc chuyên khoa {specialtyName}</h2>
                </div>

                {loading && (
                    <div style={{ textAlign: "center", marginTop: "40px" }}>
                        <MySpinner />
                    </div>
                )}

                {doctors.length === 0 && !loading && (
                    <Alert variant="warning" className="mt-4 text-center" style={{ fontWeight: "bold", fontSize: "16px" }}>
                        Khoa hiện tại không có Bác Sĩ nào.
                    </Alert>
                )}

                <div className="feature-grid" style={{ marginTop: "20px" }}>
                    {!loading && doctors.map(d => (
                        <div className="feature-card" key={d.doctorId} style={{ display: "flex", flexDirection: "column", height: "100%" }}>
                            <img 
                                className="specialty-img" 
                                src={d.image || "https://via.placeholder.com/300x220?text=Bac+Si"} 
                                alt={d.fullName} 
                                style={{ height: "220px", objectFit: "cover" }}
                            />
                            
                            <h3 className="card-title-shared" style={{ marginTop: "15px" }}>
                                <strong>{d.fullName}</strong>
                            </h3>
                            
                            <p className="card-text-shared">
                                Kinh nghiệm: {d.experienceYears} năm trong nghề.
                            </p>
                            
                            <div className="card-actions-shared">
                                <button onClick={() => handleBooking(d.doctorId)} className="btn-action-shared">
                                    Đặt lịch hẹn
                                </button>
                                
                                <button onClick={() => nav(`/doctor/${d.doctorId}`)} className="btn-outline-shared">
                                    Xem chi tiết
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                {!loading && (
                    <div style={{ textAlign: "center", marginTop: "50px", marginBottom: "20px" }}>
                        <button 
                            className="btn-outline-shared" 
                            onClick={() => nav("/specialty")} 
                            style={{ height: "45px", padding: "0 30px", fontWeight: "bold" }}
                        >
                            ⬅️ Quay lại chuyên khoa
                        </button>
                    </div>
                )}

            </div>
        </div>
    );
};

export default DoctorBySpecialty;