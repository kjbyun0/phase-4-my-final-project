import { useEffect, useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { Form, FormField, Input, Dropdown, TextArea, Button } from 'semantic-ui-react';

function NewJobPosting() {
    const [ categories, setCagetories ] = useState([]);
    const { signInAccount, onSetSignInAccount } = useOutletContext();

    // => I need to move this to app.js and share it usig useOutletContext...
    useEffect(() => {
        fetch('/jobcategories')
        .then(r => r.json())
        .then(data => setCagetories(data))
    }, []);

    const formSchema = yup.object().shape({
        title: yup.string().required("Must enter a title"),
        salary: yup.number().positive('Must be a positive number'),
    });

    const formik = useFormik({
        initialValues: {
            title: '',
            category: 'Cleaner', // => temporary hard coding initialization....
            description: '',
            salary: 0.0,
            job_type: 'Full time',
            remote: 'On-Site',
            is_active: true,
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            fetch('/jobpostings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(values)
            })
            .then(r => {
                if (r.ok) {
                    alert('New Job Posted');
                    // formik.resetForm();
                } else
                    alert('Error posting the new job');
            });
        },
    });

    return (
        <Form onSubmit={formik.handleSubmit}>
            <FormField inline>
                <label>Job Title:</label>
                <Input id='title' name='title' type='text' value={formik.values.title}
                    onChange={formik.handleChange} onBlur={formik.handleBlur} />
                <p style={{ color: 'red', }}>{formik.touched.title ? formik.errors.title : null}</p>
            </FormField>
            <FormField inline>
                <label>Job Category:</label>
                <Dropdown selection search value={formik.values.category} 
                    onChange={(e, selVal) => formik.setFieldValue('category', selVal.value)}  
                    options={categories.map(category => ({
                        key: category.id, 
                        value: category.category, 
                        text: category.category,
                    }))} 
                />
            </FormField>
            <FormField inline>
                <label>Pay:</label>
                <Input id='salary' name='salary' type='number' value={formik.values.salary} 
                    onChange={formik.handleChange} onBlur={formik.handleBlur} />
                <p style={{ color: 'red', }}>{formik.touched.salary ? formik.errors.salary : null}</p>
            </FormField>
            <FormField inline>
                <label>Job Type:</label>
                <Dropdown selection value={formik.values.job_type} 
                    onChange={(e, selVal) => formik.setFieldValue('job_type', selVal.value)}
                    options={[
                        {key: 'f', value: 'Full time', text: 'Full time'}, 
                        {key: 'p', value: 'Part time', text: 'Part time'}, 
                        {key: 'c', value: 'Contract', text: 'Contract'}, 
                    ]} 
                />
            </FormField>
            <FormField inline>
                <label>Remote:</label>
                <Dropdown selection value={formik.values.remote}
                    onChange={(e, selVal) => formik.setFieldValue('remote', selVal.value)} 
                    options={[
                        {key: 'o', value: 'On-Site', text: 'On-Site'}, 
                        {key: 'r', value: 'Remote', text: 'Remote'}, 
                        {key: 'h', value: 'Hybrid', text: 'Hybrid'},
                    ]} 
                />
            </FormField>
            <FormField inline>
                <label>Descriptions</label>
                <TextArea id='description' name='description' rows='10' utocorrect='on' 
                    value={formik.values.description} onChange={formik.handleChange} />
            </FormField>
            <Button type='submit'>Submit</Button>
        </Form>

    );
}

export default NewJobPosting;
