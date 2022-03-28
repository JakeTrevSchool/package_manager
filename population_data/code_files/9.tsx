import React from "react";
import type { FC } from "react";
import Line from "./Line";
import type { scannedLineObject } from "latin-scanner/build/src/types";

interface outputAreaProps {
  toRender: scannedLineObject[];
}

const OutputArea: FC<outputAreaProps> = ({ toRender }) => {
  return (
    <div className="outputArea">
      <ul>
        {toRender.map((each, i) => {
          return <Line scannedLine={each} id={i} />;
        })}
      </ul>
    </div>
  );
};

export default OutputArea;
