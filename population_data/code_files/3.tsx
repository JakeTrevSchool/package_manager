import React, { FC, useState } from "react";
import "../index.scss";
import { HashRouter, Switch, Route } from "react-router-dom";
import AboutSection from "./AboutSection";
import ScanArea from "./ScanArea";
import InputOptionsBar from "./INPUTS/InputOptionsBar";
import Header from "./Header";
import { defaultSettings } from "latin-scanner";
import { CamController } from "./INPUTS/camera/CamController";
import { FileStatusModal } from "./INPUTS/file/FileStatusModal";
import { file } from "@babel/types";

const App: FC = () => {
  //the "Text" state of the app; the users input.
  //kept at top level so it can be consistent across mobile and webapp components.
  let [cameraModalOpen, setCameraModalOpen] = useState(false);
  let [fileModalOpen, setFileModalOpen] = useState(false);
  let [text, setText] = useState("");
  let [settings, setSettings] = useState(defaultSettings);
  let [picture, setPicture] = useState(new File([], "image.png"));
  let modal = cameraModalOpen ? (
    <CamController text={text} setText={setText} setOpen={setCameraModalOpen} />
  ) : fileModalOpen ? (
    <FileStatusModal
      picture={picture}
      close={() => setFileModalOpen(false)}
      setText={setText}
    />
  ) : (
    <div className="modalPlaceholder"></div>
  );

  return (
    <HashRouter>
      <div className="app">
        <Header />
        {modal}

        <Switch>
          <Route exact path="/about">
            <AboutSection />
          </Route>
          <Route path="">
            <InputOptionsBar
              setText={setText}
              setCameraOpen={setCameraModalOpen}
              setFile={(file: File) => {
                setFileModalOpen(true);
                setPicture(file);
              }}
            />
            <ScanArea
              text={text}
              setText={setText}
              settings={settings}
              setSettings={setSettings}
            />
          </Route>
        </Switch>
        <div className="mobileDeviceWarning">
          This site is not optimised for mobile. for best experience, use on a
          PC or Laptop
        </div>
      </div>
    </HashRouter>
  );
};

export default App;
