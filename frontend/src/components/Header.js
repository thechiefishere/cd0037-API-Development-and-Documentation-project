import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      score: '',
    };
  }

  componentDidUpdate() {
    const { userDetails, loggedIn } = this.props;
    if (!loggedIn) {
      return;
    }
    const { username, score } = userDetails;
    const { username: stateName, score: stateScore } = this.state;
    if (score !== stateScore || username !== stateName) {
      this.setState({ username, score });
    }
  }

  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    const { loggedIn } = this.props;
    const { username, score } = this.state;

    return (
      <div className='App-header'>
        <h1
          onClick={() => {
            this.navTo('');
          }}
        >
          Udacitrivia
        </h1>
        <h2
          onClick={() => {
            this.navTo('');
          }}
        >
          List
        </h2>
        <h2
          onClick={() => {
            this.navTo('/add');
          }}
        >
          Add
        </h2>
        <h2
          onClick={() => {
            this.navTo('/play');
          }}
        >
          Play
        </h2>
        {!loggedIn ? (
          <div className='user'>
            <h2
              onClick={() => {
                this.navTo('/login');
              }}
            >
              Login
            </h2>
            <h2
              onClick={() => {
                this.navTo('/signup');
              }}
            >
              SignUp
            </h2>
          </div>
        ) : (
          <h2
            onClick={() => {
              this.navTo('/logout');
            }}
          >
            Logout
          </h2>
        )}
        {loggedIn && (
          <p>
            Hi {username}, your score is {score}
          </p>
        )}
      </div>
    );
  }
}

export default Header;
