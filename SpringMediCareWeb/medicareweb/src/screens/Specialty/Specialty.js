import { useEffect, useState } from "react";
import MySpinner from "../../components/MySpinner";
import Apis, { endpoints } from "../../configs/Apis";
import { Alert } from "react-bootstrap"; 
import { useNavigate, useSearchParams } from "react-router-dom";

const Specialty = () => {
    const [specialties, setSpecialties] = useState([]);
    const [loading, setLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [kw, setKw] = useState(""); 
    const [q] = useSearchParams();
    const nav = useNavigate();

    const loadSpecialties = async () => {
        try {
            setLoading(true);
            let url = `${endpoints['specialties']}?page=${page}`; 

            const searchKw = q.get("kw");
            if (searchKw) {
                url = `${url}&kw=${encodeURIComponent(searchKw)}`;
            }

            let res = await Apis.get(url);
            
            if (res.data.length === 0 || res.data.length < 8) {
                setPage(0); 
            }
            
            if (page === 1) {
                setSpecialties(res.data);
            } else if (page > 1) {
                setSpecialties([...specialties, ...res.data]);
            }
        } catch (ex) {
            console.error("Lỗi khi tải danh sách chuyên khoa:", ex);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (page > 0) {
            loadSpecialties();
        }
    }, [q, page]);

    useEffect(() => {
        setPage(1);
        setKw(q.get("kw") || ""); 
    }, [q]);

    const loadMore = () => {
        if (page > 0 && !loading) {
            setPage(page + 1);
        }
    };

    const handleSearch = (e) => {
        e.preventDefault();
        if (kw.trim()) {
            nav(`/specialty?kw=${kw.trim()}`);
        } else {
            nav("/specialty");
        }
    };

    return (
        <div className="main-content">
            <div className="container">
                
                <div className="search-container-shared">
                    <form onSubmit={handleSearch} className="search-form-shared">
                        <input 
                            type="text" 
                            className="search-input-shared"
                            placeholder="Nhập tên chuyên khoa cần tìm..." 
                            value={kw}
                            onChange={(e) => setKw(e.target.value)}
                        />
                        <button type="submit" className="btn-main-shared">
                            Tìm kiếm
                        </button>
                    </form>
                </div>

                <div className="section-box">
                    <h2>Danh mục chuyên khoa</h2>
                    <p style={{ color: "red", fontWeight: "bold", marginBottom: "14px" }}>
                        Số lượng hiển thị: <span>{specialties.length}</span> chuyên khoa
                    </p>
                </div>

                {specialties.length === 0 && !loading && (
                    <Alert variant="warning" className="mt-2">
                        Không tìm thấy chuyên khoa nào phù hợp với từ khóa của bạn.
                    </Alert>
                )}

                <div className="feature-grid">
                    {specialties.map(s => (
                        <div className="feature-card" key={s.specialtyId} style={{ display: "flex", flexDirection: "column", height: "100%" }}>
                            
                            <img 
                                className="specialty-img" 
                                src={s.image || "https://via.placeholder.com/300x220?text=Chuyen+Khoa"} 
                                alt={s.name} 
                            />
                            
                            <h3 className="card-title-shared">
                                <strong>{s.name}</strong>
                            </h3>
                            
                            <p className="card-text-shared">
                                {s.description || "Chưa có mô tả chi tiết cho chuyên khoa này."}
                            </p>
                            
                            <div className="card-actions-shared" style={{ marginTop: "auto" }}>
                                <button 
                                    onClick={() => nav(`/specialties/${s.specialtyId}/doctors`)} 
                                    className="btn-main-shared"
                                    style={{ width: "100%", height: "40px" }}
                                >
                                    Xem bác sĩ thuộc khoa
                                </button>
                                
                                <button 
                                    onClick={() => nav(`/specialties/${s.specialtyId}`)}
                                    className="btn-outline-shared"
                                    style={{ height: "40px", display: "flex", alignItems: "center", justifyContent: "center" }}
                                >
                                    Xem chi tiết khoa
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                {loading && (
                    <div style={{ textAlign: "center", marginTop: "20px" }}>
                        <MySpinner />
                    </div>
                )}

                {page > 0 && specialties.length > 0 && !loading && (
                    <div style={{ textAlign: "center", marginTop: "44px" }}>
                        <button 
                            className="register-big-btn" 
                            onClick={loadMore}
                            style={{ width: "auto", padding: "12px 48px", display: "inline-block" }}
                        >
                            Xem thêm...
                        </button>
                    </div>
                )}
                
            </div>
        </div>
    );
};

export default Specialty;