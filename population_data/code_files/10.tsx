import React from "react";
import type { FC } from "react";
import Tooltip from "../ICONS/Tooltip";
import { misc, meterAndStatusIcons } from "../ICONS/ICONS";
import type { meter, scanStatus } from "latin-scanner/build/src/types";

interface SelectionProps {
  toggleOpen: CallableFunction;
  status: scanStatus;
  statusMessage: string;
  meter: meter;
}

const Selection: FC<SelectionProps> = ({
  toggleOpen,
  status,
  statusMessage,
  meter,
  children,
}) => {
  let isMobile = /Mobi|Android/i.test(navigator.userAgent); //dont display for mobile.
  let DownArrow = isMobile ? null : misc.DownArrow;
  return (
    <div onClick={() => toggleOpen()} className={"scanSelection " + status}>
      {DownArrow}
      <div className="outputText">{children}</div>
      <Tooltip tooltip={statusMessage}>
        {meterAndStatusIcons[meter][status]}
      </Tooltip>
    </div>
  );
};

export default Selection;
