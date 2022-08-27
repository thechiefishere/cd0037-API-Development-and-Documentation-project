import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
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
      </div>
    );
  }
}

export default Header;
