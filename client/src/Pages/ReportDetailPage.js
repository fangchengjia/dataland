import React, { Component } from 'react'
import PropTypes from 'prop-types'

export default class ReportDetailPage extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		const {match} = this.props;
		return (
			<div>
				I am report detail {match.params.id}
			</div>
		)
	}
}