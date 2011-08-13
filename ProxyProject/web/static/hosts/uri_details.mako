<table>
    <tr>
        <th>Name</th><th>Value</th>
    </tr>
%for name, value in locals().items():
    <tr>
        <td>${name|u}</td><td><pre>${value}</pre></td>
    </tr>
% endfor

</table>