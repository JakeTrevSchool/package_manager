import React from "react";
import type { FC } from "react";
import type { settingsSetter } from "../projectTypes";
import type { meter, scanSettingsObject } from "latin-scanner/build/src/types";

interface settingsBarProps {
  settings: scanSettingsObject;
  setSettings: settingsSetter;
}

const SettingsBar: FC<settingsBarProps> = ({ settings, setSettings }) => {
  function setMeter(meter: meter) {
    let temp = { ...settings };
    temp.meter = meter;
    temp.elegaic = false;
    setSettings(temp);
  }

  function switchFirstMeter() {
    let temp = { ...settings };
    temp.meter = temp.meter === "Hexameter" ? "Pentameter" : "Hexameter";
    setSettings(temp);
  }

  function setElegaic() {
    let temp = { ...settings };
    temp.elegaic = true;
    temp.meter = "Hexameter";
    setSettings(temp);
  }

  let firstMeterDisplay = settings.elegaic
    ? `${settings.meter.substring(0, 3)}. 1st`
    : "Hex. 1st";
  return (
    <div className="optionsBox">
      <button
        className={`optionButton ${
          !settings.elegaic && settings.meter === "Hexameter"
            ? "selectedMeter"
            : ""
        }`}
        onClick={() => setMeter("Hexameter")}
      >
        Hexameter
      </button>

      <button
        className={`optionButton ${
          !settings.elegaic && settings.meter === "Pentameter"
            ? "selectedMeter"
            : ""
        }`}
        onClick={() => setMeter("Pentameter")}
      >
        Pentameter
      </button>

      <button
        className={`optionButton ${settings.elegaic ? "selectedMeter" : ""}`}
        onClick={setElegaic}
      >
        Elegaic
      </button>

      <button
        className={`optionButton ${settings.elegaic ? "selectedMeter" : ""}`}
        disabled={!settings.elegaic}
        onClick={switchFirstMeter}
      >
        {firstMeterDisplay}
      </button>
    </div>
  );
};

export default SettingsBar;
