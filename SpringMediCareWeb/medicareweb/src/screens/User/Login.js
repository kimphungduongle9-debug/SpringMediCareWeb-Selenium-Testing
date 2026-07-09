import { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import cookies from "react-cookies";
import APIs, { authApis, endpoints } from "../../configs/Apis";
import { MyUserContext } from "../../configs/Contexts";

const Login = () => {
  const [, dispatch] = useContext(MyUserContext);
  const nav = useNavigate();

  const [user, setUser] = useState({
    username: "",
    password: "",
  });

  const [err, setErr] = useState("");

  const change = (e, field) => {
    setUser({ ...user, [field]: e.target.value });
  };

  const login = async (e) => {
    e.preventDefault();

    try {
      const res = await APIs.post(endpoints.login, {
        username: user.username,
        password: user.password,
      });

      cookies.save("token", res.data.token);

      const profile = await authApis().get(endpoints["current-user"]);

      cookies.save("user", profile.data);

      dispatch({
        type: "LOGIN",
        payload: profile.data,
      });

      nav("/");
    } catch (ex) {
      console.error(ex);
      setErr("Sai tên đăng nhập hoặc mật khẩu");
    }
  };

  return (
    <div className="login-center-wrap">
      <div className="login-pastel-box">
        <div className="login-head-box">
          <span className="login-label-chip">TÀI KHOẢN BỆNH NHÂN</span>
          <h2>Đăng nhập</h2>
          <p>
            Đăng nhập để đặt lịch khám, xem lịch sử khám và sử dụng các chức
            năng của hệ thống.
          </p>
        </div>

        {err && <p className="login-error-text">{err}</p>}

        <form onSubmit={login}>
          <div className="login-field-box">
            <label>Tên đăng nhập hoặc email</label>
            <input
              type="text"
              value={user.username}
              onChange={(e) => change(e, "username")}
              placeholder="Nhập tên đăng nhập hoặc email"
              required
            />
          </div>

          <div className="login-field-box">
            <label>Mật khẩu</label>
            <input
              type="password"
              value={user.password}
              onChange={(e) => change(e, "password")}
              placeholder="Nhập mật khẩu"
              required
            />
          </div>

          <button type="submit" className="login-big-btn">
            Đăng nhập
          </button>
        </form>

        <p className="login-register-line">
          Chưa có tài khoản? <Link to="/register">Đăng ký ngay</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
