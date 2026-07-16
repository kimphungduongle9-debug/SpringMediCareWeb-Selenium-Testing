import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import APIs, { endpoints } from "../../configs/Apis";

const Register = () => {
  const nav = useNavigate();

  const [user, setUser] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    username: "",
    password: "",
    confirmPassword: "",
    role: "patient",
  });

  const [avatar, setAvatar] = useState(null);
  const [err, setErr] = useState("");

  const change = (e, field) => {
    setUser({ ...user, [field]: e.target.value });
  };

  const register = async (e) => {
    e.preventDefault();

    if (!/^\d{10}$/.test(user.phone)) {
      setErr("Số điện thoại phải gồm đúng 10 chữ số");
      return;
    }

    if (user.password.length < 7) {
      setErr("Mật khẩu phải có ít nhất 7 ký tự");
      return;
    }

    if (!/[A-Z]/.test(user.password)) {
      setErr("Mật khẩu phải chứa ít nhất 1 chữ in hoa");
      return;
    }

    if (!/[a-z]/.test(user.password)) {
      setErr("Mật khẩu phải chứa ít nhất 1 chữ thường");
      return;
    }

    if (!/[0-9]/.test(user.password)) {
      setErr("Mật khẩu phải chứa ít nhất 1 chữ số");
      return;
    }

    if (!/[^A-Za-z0-9\s]/.test(user.password)) {
      setErr("Mật khẩu phải chứa ít nhất 1 ký tự đặc biệt");
      return;
    }
    if (user.password !== user.confirmPassword) {
      setErr("Mật khẩu xác nhận không khớp");
      return;
    }

    if (avatar === null) {
      setErr("Vui lòng chọn ảnh đại diện");
      return;
    }

    try {
      let form = new FormData();

      form.append("firstName", user.firstName);
      form.append("lastName", user.lastName);
      form.append("email", user.email);
      form.append("phone", user.phone);
      form.append("username", user.username);
      form.append("password", user.password);
      form.append("role", user.role);
      form.append("avatar", avatar);

      await APIs.post(endpoints.users, form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      nav("/login");
    } catch (ex) {
      console.error(ex);
      setErr("Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.");
    }
  };

  return (
    <div className="register-center-wrap">
      <div className="register-pastel-box">
        <div className="register-head-box">
          <span className="register-label-chip">TÀI KHOẢN BỆNH NHÂN</span>
          <h2>Đăng ký</h2>
          <p>Tạo tài khoản để đặt lịch khám và theo dõi hồ sơ khám bệnh.</p>
        </div>

        {err && <p className="register-error-text">{err}</p>}

        <form onSubmit={register}>
          <div className="register-grid-2">
            <div className="register-field-box">
              <label>Họ</label>
              <input
                type="text"
                value={user.firstName}
                onChange={(e) => change(e, "firstName")}
                required
              />
            </div>

            <div className="register-field-box">
              <label>Tên</label>
              <input
                type="text"
                value={user.lastName}
                onChange={(e) => change(e, "lastName")}
                required
              />
            </div>
          </div>

          <div className="register-field-box">
            <label>Email</label>
            <input
              type="email"
              value={user.email}
              onChange={(e) => change(e, "email")}
              required
            />
          </div>

          <div className="register-field-box">
            <label>Số điện thoại</label>
            <input
              type="text"
              value={user.phone}
              onChange={(e) => change(e, "phone")}
              required
            />
          </div>

          <div className="register-field-box">
            <label>Tên đăng nhập</label>
            <input
              type="text"
              value={user.username}
              onChange={(e) => change(e, "username")}
              required
            />
          </div>

          <div className="register-grid-2">
            <div className="register-field-box">
              <label>Mật khẩu</label>
              <input
                type="password"
                value={user.password}
                onChange={(e) => change(e, "password")}
                required
              />
            </div>

            <div className="register-field-box">
              <label>Xác nhận mật khẩu</label>
              <input
                type="password"
                value={user.confirmPassword}
                onChange={(e) => change(e, "confirmPassword")}
                required
              />
            </div>
          </div>

          <div className="register-field-box">
            <label>Ảnh đại diện</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setAvatar(e.target.files[0])}
              required
            />
          </div>

          <button type="submit" className="register-big-btn">
            Đăng ký
          </button>
        </form>

        <p className="register-login-line">
          Đã có tài khoản? <Link to="/login">Đăng nhập ngay</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
