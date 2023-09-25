export const helpHttp = () =>{
    const customFetch = (endpoit,options) => {
        const defaultHeader ={
            accept:"application/json",
        }
        

        options.method = options.method || "GET";
        options.headers = options.headers
        ?{...defaultHeader,...options.headers}
        :defaultHeader;

        options.body = JSON.stringify(options.body)|| false

        if(!options.body)delete options.body
    
        return(
            fetch(endpoit,options).then((res)=>res.ok?res.json()
                :Promise.reject({ err:true,
                detail:res.detail || "not detail",
                status:res.status || "error personalizado",
                statusText:res.statusText || "error text personalizado"
                })
            .catch((err)=>err)
        ))
    }

    const get = (url,options={}) => customFetch(url,options)
    const post = (url,options={}) =>{
        options.method = "POST";
        return customFetch(url,options)
    }
    const put = (url,options={}) =>{
        options.method = "PUT";
        return customFetch(url,options)
    }
    const del = (url,options={}) =>{
        options.method = "DELETE";
        return customFetch(url,options)
    }

    return{
        get,
        post,
        put,
        del,
    };
}
