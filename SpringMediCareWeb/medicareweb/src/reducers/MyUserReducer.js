import cookies from "react-cookies";

const MyUserReducer = (current, action) => {
  switch (action.type) {
    case "LOGIN":
      return action.payload;

    case "LOGOUT":
      cookies.remove("token");
      cookies.remove("user");
      return null;

    default:
      return current;
  }
};

export default MyUserReducer;
