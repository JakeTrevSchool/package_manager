import React from "react";
import type { FC } from "react";
import { Link } from "react-router-dom";

const Header: FC = () => {
  return (
    <div className="header">
      <Link to="/about">
        <h1 className="headerItem">About</h1>
      </Link>
      <Link to="/">
        <h1 className="headerItem">Latin Scan</h1>
      </Link>
      <Link to="/">
        <h1 className="headerItem"></h1>
      </Link>
    </div>
  );
};

export default Header;
