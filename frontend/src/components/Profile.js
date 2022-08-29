import React, { Component } from 'react';
import { FaRegUserCircle } from 'react-icons/fa';
import { withRouter } from 'react-router-dom';

import '../stylesheets/Profile.css';

export class Profile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      score: '',
      answeredQuestions: [],
    };
  }
  async componentDidMount() {
    const { loggedIn, userDetails } = this.props;
    if (loggedIn) {
      const { username: name, token } = userDetails;
      try {
        const response = await fetch(`users/${name}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        const { username, score, answered_questions } = data;
        this.setState({
          username,
          score,
          answeredQuestions: answered_questions,
        });
      } catch (error) {
        console.log(error);
      }
    }
  }
  render() {
    const { username, score, answeredQuestions } = this.state;
    return (
      <section className='Profile'>
        <div>
          <div className='Profile-Icon'>{<FaRegUserCircle />}</div>
          <p>You are welcome {username}</p>
          <p>Your score is {score}</p>
        </div>
        <div className='Profile-Questions'>
          <h3>Answered Questions</h3>
          <ul>
            {answeredQuestions.map((ques) => (
              <li key={ques.id}>{ques.question}</li>
            ))}
          </ul>
        </div>
      </section>
    );
  }
}

export default withRouter(Profile);
