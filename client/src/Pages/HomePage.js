import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Avatar from '@material-ui/core/Avatar';
import ImageIcon from '@material-ui/icons/Image';
import WorkIcon from '@material-ui/icons/Work';
import BeachAccessIcon from '@material-ui/icons/BeachAccess';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import SanpbioAppBar from './components/SnapbioAppBar';

const styles = theme => ({
	root: {
    flexGrow: 1,
  },
  listcontainer: {
    width: '100%',
    // maxWidth: 1080,
    backgroundColor: theme.palette.background.paper,
	},
  paper: {
    padding: theme.spacing.unit * 2,
    textAlign: 'center',
    color: theme.palette.text.secondary,
	},
	header: {
		textAlign: 'left'
	}
});

class HomePage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			reportedItems: []
		}
	}

	createList(){
		const {classes, history} = this.props;
		return (
			<div className={classes.listcontainer}>
				<List>
					<ListItem button onClick={() => history.push('report/' + 1)}>
						<Avatar style={{backgroundColor:'#FF6F00'}}>
							<ImageIcon />
						</Avatar>
						<ListItemText primary="Photos" secondary="Jan 9, 2014" />
					</ListItem>
					<ListItem>
						<Avatar>
							<WorkIcon />
						</Avatar>
						<ListItemText primary="Work" secondary="Jan 7, 2014" />
					</ListItem>
					<ListItem>
						<Avatar>
							<BeachAccessIcon />
						</Avatar>
						<ListItemText primary="Vacation" secondary="July 20, 2014" />
					</ListItem>
				</List>
			</div>
		)
	}

	render() {
		const {classes} = this.props;
		return (
			<div className={classes.root}>
      	<Grid container justify="center" spacing={24}>
					<Grid className={classes.header} item xs={12}>
						<SanpbioAppBar title="Home"/>
					</Grid>
        	<Grid item xs={10}>
						<Paper className={classes.paper}>
							{this.createList()}
						</Paper>
					</Grid>
				</Grid>
			</div>
		)
	}
}

export default withStyles(styles)(HomePage)