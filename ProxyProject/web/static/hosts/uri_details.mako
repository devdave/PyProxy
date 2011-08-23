<span>
    <a href="/">Host List</a> >> <a href="/hosts/sessions/${host}">${host}</a>   
</span>
<style>
   td { width: 35%; }
</style>

%for record in uris:
<h2>Record ${ record.id} - ${record.runTime} ms</h2>
<fieldset>
    <legend>Request</legend>
    <h3>Headers</h3>
    <table>
        <thead>
            <tr>
                <th>Type</th>
                <th>Value</th>        
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>method</td>
                <td>${record.request['method']}</td>
            </tr>
%if len(record.request['data']) > 0:
            <tr>
                <td>data</td>
                <td>${record.request['data']}</td>        
            </tr>
%endif            
            <tr>
                <td>URI</td>
                <td>${record.request['uri']}</td>        
            </tr>
% for name, value in record.request['headers'].items():
            <tr>
                <td>${name}</td>
                <td>${value|h}</td>
            </tr>        
% endfor
        </tbody>
    </table>
</fieldset>

<fieldset>
    <legend>Response</legend> 
    <h3>Headers</h3>
    <table>
    <thead>
        <tr>
            <th>Name</th>
            <td>Value</th>
        </tr>
        <tbody>
% for name, value in record.response['headers'].items():
            <tr>
                <td>${name}</td>
                <td>${value|h}</td>
            </tr>        
% endfor
        </tbody>
    </table>
    <a href="/hosts/record/${record.id}">View response body</a>
</fieldset>

% endfor

