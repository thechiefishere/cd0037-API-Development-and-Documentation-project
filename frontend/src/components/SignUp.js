import React, { Component } from 'react';
import '../stylesheets/Login.css';

export default class SignUp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      password: '',
    };
  }

  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  handleSubmit = async (e) => {
    e.preventDefault();
    const { username, password } = this.state;
    const { setUserDetails } = this.props;
    if (!username || !password) {
      return;
    }
    const response = await fetch('users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });
    const data = await response.json();
    console.log('data', data);
    this.setState({ username: '', password: '' });
    setUserDetails(data);
  };

  renderSignUp() {
    return (
      <section className='SignUp-Component'>
        <div className='Component-Heading'>
          <h1>SIGNUP</h1>
          <p>Signup to play the best trivia game ever</p>
        </div>
        <form className='Form' onSubmit={(e) => this.handleSubmit(e)}>
          <div className='Form-Component'>
            <label>Username:</label>
            <input
              type='text'
              placeholder='enter username'
              value={this.state.username}
              onChange={(e) => this.setState({ username: e.target.value })}
            />
          </div>
          <div className='Form-Component'>
            <label>Password:</label>
            <input
              type='password'
              placeholder='enter password'
              value={this.state.password}
              onChange={(e) => this.setState({ password: e.target.value })}
            />
          </div>
          <input type='submit' value='SignUp' className='Submit-Btn' />
        </form>
        <div className='SignUp-Nav'>
          <p>Already registered?</p>
          <p
            onClick={() => {
              this.navTo('/login');
            }}
          >
            Login
          </p>
        </div>
      </section>
    );
  }

  render() {
    return <div className='SignUp'>{this.renderSignUp()}</div>;
  }
}
