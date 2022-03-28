import React from "react";
import type { FC } from "react";
import type { settingsSetter, stringSetter } from "../projectTypes";

import InputArea from "./InputArea";
import OutputArea from "./output/OutputArea";
import SettingsBar from "./SettingsBar";
import { scanParagraph } from "latin-scanner";
import type { scanSettingsObject } from "latin-scanner/build/src/types";

interface scanAreaProps {
  text: string;
  setText: stringSetter;
  settings: scanSettingsObject;
  setSettings: settingsSetter;
}

const ScanArea: FC<scanAreaProps> = ({
  text,
  setText,
  settings,
  setSettings,
}) => {
  let scanned = scanParagraph(text, settings);
  return (
    <div className="ScanArea">
      <SettingsBar settings={settings} setSettings={setSettings} />
      <div className="IOArea">
        <InputArea
          value={text}
          setValue={setText}
          placeholder="Enter Latin here..."
        />
        <OutputArea toRender={scanned} />
      </div>
    </div>
  );
};

export default ScanArea;
