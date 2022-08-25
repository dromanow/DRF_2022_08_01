import {Link} from 'react-router-dom'


const AuthorItem = ({author}) => {
    return (
        <tr>

            <td>
                {author.first_name}
            </td>
            <td>
                <Link to={`/authors/${author.id}`}>{author.last_name}</Link>
            </td>
            <td>
                {author.birthday_year}
            </td>
        </tr>
    )
}

const AuthorList = ({authors}) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>
                        First name
                    </th>
                    <th>
                        Last name
                    </th>
                    <th>
                        Birthday year
                    </th>
                </tr>
            </thead>
            <tbody>
                {authors.map((author) => <AuthorItem author={author} /> )}
            </tbody>
        </table>
    )
}

export default AuthorList
