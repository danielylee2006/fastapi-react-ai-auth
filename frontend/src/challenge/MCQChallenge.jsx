import "react";
import { useState } from "react";

//MCQChallenge component represents one individual question:
//Reusable componenet in for question displaying in the main and the history page.

/*MCQChallenge takes in two props:
1. challenge object that contains challenge details (question, options, ans, etc.)
2. showExplanation 
*/
export function MCQChallenge({ challenge, showExplanation = false }) {

  const [selectedOption, setSelectedOption] = useState(null); //tracks which option is chosen currently
  const [shouldShowExplanation, setShouldShowExplanation] = useState(null); //tracks whether to show explanation or not

  //makes sure thatn options is in JSON OBJ.
  const options =
    typeof challenge.options === "string"
      ? JSON.parse(challenge.options)
      : challenge.options;

/*
1. runs when user selects an option
2. if user already selected an option (selectedOption !== null) -> do nothing. 
   we don't want the user to change the answer after.
3. Set the selectedOption and set ShouldShowExplanation to true.
*/
  const handleOptionSelect = (index) => {
    if (selectedOption !== null) return;
    setSelectedOption(index);
    setShouldShowExplanation(true);
  };

 
  /*
    This functions assigns a CSS class depending on whether its correct or not

    1. If no select option yet -> default "option" class
    2. If the index and correct answer ID match up --> "option correct" class
    3. If the index does not equal the correct answer ID --> "option incorrect" class
  */
  const getOptionClass = (index) => {
    if (selectedOption === null) return "option";

    if (index === challenge.correct_answer_id) {
      return "option correct";
    }

    if (selectedOption === index && index !== challenge.correct_answer_id) {
      return "option incorrect";
    }
    return "option";
  };

  return (
    <div className="challenge-display">
      <p>
        <strong>Difficulty</strong>: {challenge.difficulty}
      </p>
      <p className="challenge-title">{challenge.title}</p>
      <div className="options">
        {options.map((option, index) => (
          <div
            className={getOptionClass(index)}
            key={index}
            onClick={() => {
              handleOptionSelect(index);
            }}
          >
            {option}
          </div>
        ))}
      </div>
      {shouldShowExplanation && selectedOption !== null && (
        <div className="explanation">
          <h4>Explanation</h4>
          <p>{challenge.explanation}</p>
        </div>
      )}
    </div>
  );
}

/*
- Challenge Display jsx

    -Within the options div we map out the options using .map()
    -each options are dynamically classed using getOptionClass.

    -Explanation is rendered when shouldShowExplanation becomes true and selectedOption actually exists
    (shouldShowExplanation becomes true when user selects option which calls handleSelectedOption)

*/
