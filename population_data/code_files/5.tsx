import { replaceForcedQuantities } from "latin-scanner";
import React, { FC, useEffect, useRef, useState } from "react";
import type { stringSetter } from "../projectTypes";

function setCaretPos(elRef: HTMLTextAreaElement, pos: number) {
  if (elRef.setSelectionRange) {
    elRef.focus();
    elRef.setSelectionRange(pos, pos);
  }
}

//*main
interface inputAreaProps {
  value: string;
  setValue: stringSetter;
  placeholder: string;
}

//aka autoheight text area
let InputArea: FC<inputAreaProps> = ({ value, setValue, placeholder }) => {
  let [caretPos, storeCaretPos] = useState(0);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function handleTextChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    let caretPosition = e.target.selectionStart - 1;
    let text = e.target.value;
    let handledText = replaceForcedQuantities(text);
    if (handledText !== text) {
      storeCaretPos(caretPosition);
    }
    setValue(handledText);
  }

  //when the component is re-rendered with a new value, recalculate and update the height
  useEffect(() => {
    if (textareaRef.current !== null) {
      textareaRef.current.style.height = "0px";
      const scrollHeight = textareaRef.current.scrollHeight;
      textareaRef.current.style.height = scrollHeight + "px";
    }
  }, [value]);

  //when a user forces a vowel quantity, ensure that the caret/cursor does not move to the end.
  useEffect(() => {
    if (textareaRef.current !== null) {
      setCaretPos(textareaRef.current, caretPos);
    }
  }, [caretPos]);

  return (
    <textarea
      autoFocus
      ref={textareaRef}
      value={value}
      placeholder={placeholder}
      onChange={handleTextChange}
      className="inputArea"
    />
  );
};
export default InputArea;
