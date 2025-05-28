process call_snvs {
    tag "$sample_id"
    container 'quay.io/biocontainers/lofreq:2.1.5--py38h794fc9e_10'
    publishDir "${params.outdir}/$sample_id/variants/", mode: 'copy'                              


    input:
        tuple(val(sample_id), path("${sample_id}.bam"), path("${sample_id}.bam.bai"), path(reference))
        path(bed)

    output:
        tuple(val(sample_id), path("${sample_id}.snv.vcf") , emit: snv)
        tuple(val(sample_id), path("${sample_id}.clinical.snv.vcf") , emit: clinical_snv)
        path  "versions.yml"                            , emit: versions
 
  script:
    """
    # ---------------
    # Variant calling
    # ---------------


    # use lofreq to call variants
    lofreq index ${sample_id}.bam
    lofreq faidx ${reference}

    # lofreq call to quantify variant frequencies 
    lofreq call-parallel --pp-threads 4 -B --no-default-filter -f "${reference}" -o ${sample_id}.pre_vcf -l "${bed}" ${sample_id}.bam

    # filter for quality research
    lofreq filter -a ${params.percent_mutations} --no-defaults -i  ${sample_id}.pre_vcf -o ${sample_id}.snv.vcf

    # filter for clinical research
    lofreq filter -a ${params.percent_mutations_clinical} --no-defaults -i  ${sample_id}.pre_vcf -o ${sample_id}.clinical.snv.vcf
    
    # Versions #
    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        lofreq: \$(echo \$(lofreq version 2>&1) | sed 's/^version: //; s/ *commit.*\$//')
    END_VERSIONS

    """
}