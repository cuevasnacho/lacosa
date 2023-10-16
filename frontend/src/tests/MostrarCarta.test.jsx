import { render,screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import MostrarCarta from '../components/MostrarCarta/MostrarCarta.jsx';


test('src analisis con exito', () => {
    const nombreCarta="analisis"
    const src='analisis.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src lacosa con exito', () => {
    const nombreCarta="lacosa"
    const src='lacosa.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src cuerdas_podridas con exito', () => {
    const nombreCarta="cuerdas_podridas"
    const src='cuerdas_podridas.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src aterrador con exito', () => {
    const nombreCarta="aterrador"
    const src='aterrador.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src aqui_estoy_bien con exito', () => {
    const nombreCarta="aqui_estoy_bien"
    const src='aqui_estoy_bien.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src cambio_de_lugar con exito', () => {
    const nombreCarta="cambio_de_lugar"
    const src='cambio_de_lugar.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src cuarentena con exito', () => {
    const nombreCarta="cuarentena"
    const src='cuarentena.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src determinacion con exito', () => {
    const nombreCarta="determinacion"
    const src='determinacion.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src fallaste con exito', () => {
    const nombreCarta="fallaste"
    const src='fallaste.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src hacha con exito', () => {
    const nombreCarta="hacha"
    const src='hacha.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src infectado con exito', () => {
    const nombreCarta="infectado"
    const src='infectado.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src lanzallamas con exito', () => {
    const nombreCarta="lanzallamas"
    const src='lanzallamas.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })

  test('src mas_vale_que_corras con exito', () => {
    const nombreCarta="mas_vale_que_corras"
    const src='mas_vale_que_corras.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src nada_de_barbacoas con exito', () => {
    const nombreCarta="nada_de_barbacoas"
    const src='nada_de_barbacoas.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src no_gracias con exito', () => {
    const nombreCarta="no_gracias"
    const src='no_gracias.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src puerta_atrancada con exito', () => {
    const nombreCarta="puerta_atrancada"
    const src='puerta_atrancada.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src seduccion con exito', () => {
    const nombreCarta="seduccion"
    const src='seduccion.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src vigila_tus_espaldas con exito', () => {
    const nombreCarta="vigila_tus_espaldas"
    const src='vigila_tus_espaldas.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src whisky con exito', () => {
    const nombreCarta="whisky"
    const src='whisky.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src cita_a_ciegas con exito', () => {
    const nombreCarta="cita_a_ciegas"
    const src='cita_a_ciegas.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src es_aqui_la_fiesta con exito', () => {
    const nombreCarta="es_aqui_la_fiesta"
    const src='es_aqui_la_fiesta.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src no_podemos_ser_amigos con exito', () => {
    const nombreCarta="no_podemos_ser_amigos"
    const src='no_podemos_ser_amigos.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src olvidadizo con exito', () => {
    const nombreCarta="olvidadizo"
    const src='olvidadizo.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src que_quede_entre_nosotros con exito', () => {
    const nombreCarta="que_quede_entre_nosotros"
    const src='que_quede_entre_nosotros.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src revelaciones con exito', () => {
    const nombreCarta="revelaciones"
    const src='revelaciones.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src sal_de_aqui con exito', () => {
    const nombreCarta="sal_de_aqui"
    const src='sal_de_aqui.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src tres_cuatro con exito', () => {
    const nombreCarta="tres_cuatro"
    const src='tres_cuatro.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src uno_dos con exito', () => {
    const nombreCarta="uno_dos"
    const src='uno_dos.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src ups con exito', () => {
    const nombreCarta="ups"
    const src='ups.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src vuelta_y_vuelta con exito', () => {
    const nombreCarta="vuelta_y_vuelta"
    const src='vuelta_y_vuelta.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src back_alejate con exito', () => {
    const nombreCarta="back_alejate"
    const src='back_alejate.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src back_panico con exito', () => {
    const nombreCarta="back_panico"
    const src='back_panico.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })
  test('src misteriosa con exito', () => {
    const nombreCarta="misteriosa"
    const src='misteriosa.png'
    const img = render(<MostrarCarta nombreCarta={nombreCarta}/>)
    const imgRender =  img.getByRole('img')
    expect(imgRender).toBeInTheDocument();
    expect(imgRender).toHaveAttribute('src',src)
  })