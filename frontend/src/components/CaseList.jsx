import React from 'react';
import { Link } from 'react-router-dom';

const CaseList = ({ cases }) => {
    if (!cases || cases.length === 0) {
        return <p>No cases found.</p>;
    }

    return (
        <ul>
            {cases.map((caseItem) => (
                <li key={caseItem.case_id}>
                    <Link to={`/case/${caseItem.case_id}`}>
                        <strong>{caseItem.case_name}</strong>
                    </Link>
                    - Status: {caseItem.status}
                    (Created: {new Date(caseItem.created_at).toLocaleDateString()})
                </li>
            ))}
        </ul>
    );
};

export default CaseList;
