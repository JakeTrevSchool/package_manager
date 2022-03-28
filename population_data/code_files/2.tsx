import React from "react";
import type { FC } from "react";
import { Route } from "react-router-dom";
import About from "./About";

const AboutSection: FC = () => {
  return (
    <Route exact path="/about">
      <div className="aboutArea">
        <h1 className="title">About Latin-Scan</h1>
        <About title="Where am I?">
          Latin-Scan.com is an automatic latin scansion tool - if you don't
          already know what that means, it's probably not for you. It is a hobby
          project of one person.
        </About>
        <About title="What is Scansion?">
          Scansion is the process of determining the meter (rhythm) of poetry.
          In latin, this is done through a combination of following some rules,
          and a process of elimination. First, you determine the "quantity" or
          length for every vowel in the line you can. You then compare this to a
          small number of patterns that the line could take on. The pattern you
          have left (and hopefully, it will only be one) is that line's rhythm.
        </About>
        <About title="What are the Rules?">
          <a
            href="http://www.thelatinlibrary.com/satire/scansion.pdf"
            target="_blank"
            className="visibleLink"
          >
            This PDF
          </a>{" "}
          is a good place to start. It explains the rules for quantity (which
          are applicable across all kinds of poetry), and the patterns which
          make up Hexameter verse.
        </About>
        <About title="Usage">
          Before you begin, ensure that you have the correct meter selected at
          the top. If you are scanning elegaic couplets, check that the meter
          for the first line is set correctly too. When you enter text, an
          output will be generated on the right. The symbol on the far right
          will indicate the status for that line. Clicking on a line in the
          output will allow you to see all the information about that line at
          once - you can select which version you want to diplay by clicking on
          it.
          <h3>forcing vowels</h3>
          You can also force a vowel to take on a given quantity. Simply type
          "_" (underscore) before a vowel to make it long, or "@" (at) before a
          vowel to make it short. This can be useful if the line isn't scanning
          right.
        </About>
        <About title="Alternative input methods">
          <p>
            With the newest version of Latin-Scan.com, there are now several
            options for how to input the text you wish to scan. If your device
            supports it, you can now upload a file or take a picture of the text
            to scan. Even if you don’t have a camera, you can still upload
            images – simply click the file upload button and select the file you
            wish to upload, be it a PNG or a JPEG. Text detection is powered by{" "}
            <a
              href="https://tesseract.projectnaptha.com/"
              target="_blank"
              className="visibleLink"
            >
              tesseract.js.
            </a>
          </p>
          <p>
            Unfortunately, not all file types are supported. Word files (.docs,
            .docx) are difficult to read, as are PDFs. Please rest assured that
            I am working on adding support for those files. If you are trying to
            upload a word file, I recommend saving it as a .txt file and
            uploading that. If that is not possible, or if you are working with
            a PDF then I suggest copy-pasting the text.
          </p>
        </About>
        <About title="Capabilities">
          Unfortunatley, the system behind latin-scan.com is not perfect. It
          cannot, as a rule, detect vowels that have quantity by nature; many of
          these require checking if a word is of a specific class (for instance,
          a first declension ablative noun with an -a ending). This kind of
          check is much harder to implement, and so it is unlikely I will ever
          be able to implement it. As a rule, modifications to how quantity is
          detected is not possible.
          <p>
            It is also very difficult to deal with situations where a poet has
            broken the rules. The opening of Virgil's eclogue 1 is a good
            example of this, where the word "patriae" contains a long-short-long
            pattern that cannot be scanned. This can be fixed however, by
            forcing the quantity of one of the concerned vowels. On the upside:
            I am still working on this site, so it should always be improving.
          </p>
        </About>
        <About title="Credits">
          The Icons used in this project were created by{" "}
          <a
            href="https://fontawesome.com/"
            target="_blank"
            className="visibleLink"
          >
            Font Awesome
          </a>{" "}
          under their{" "}
          <a
            href="https://fontawesome.com/license"
            target="_blank"
            className="visibleLink"
          >
            license.
          </a>
        </About>
      </div>
    </Route>
  );
};

export default AboutSection;
